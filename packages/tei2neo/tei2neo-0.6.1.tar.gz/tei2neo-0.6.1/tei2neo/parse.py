# pylint: disable=too-many-lines
import inspect
import keyword
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

import spacy
from bs4 import BeautifulSoup, Comment
from lxml import etree
from py2neo import Node, Relationship

assert sys.version_info >= (3, 8)  # at least Python 3.8 or higher

nlp = spacy.load("de_core_news_sm")


def get_categories(tei_node):
    """searches the TEI document for catRef
    and looks it up in the taxonomy/category definition
    returns a list of categories
    """
    categories = []
    catref_node = tei_node.find("catRef")
    if not catref_node:
        return categories
    catref_node = tei_node.find("catRef")
    for catref in catref_node.attrs.get("target", "").split():
        *_, xml_id = catref.split("#")
        cat = tei_node.find(attrs={"xml:id": xml_id})
        if cat:
            for catdesc in cat.find_all("catDesc"):
                categories.append(catdesc.string)
    return categories


def import_categories(filename, tx):
    """This procedure reads a TEI file containing the categories
    and writes them as (:category)-[HAS_DESCRIPTION]->(:catDesc)
    node-pairs to the TEI database.
    """

    def extract_information(cats, filename):
        all_cats = []
        for cat in cats.find_all("category"):
            catDescs = []
            for catDesc in cat.find_all("catDesc"):
                catDescs.append(
                    {"language": catDesc.get("xml:lang"), "description": catDesc.text}
                )

            all_cats.append(
                {
                    "label": "category",
                    "attrs": {"xml:id": cat.get("xml:id"), "filename": filename},
                    "catDescs": catDescs,
                }
            )
        return all_cats

    def create_nodes_from_cats(cats, tx):
        for cat in cats:
            cat_node = Node(cat["label"], **cat["attrs"])
            tx.create(cat_node)
            for catDesc in cat["catDescs"]:
                desc_node = Node("catDesc", **catDesc)
                tx.create(desc_node)
                rel = Relationship(
                    cat_node,
                    "HAS_DESCRIPTION",
                    desc_node,
                )
                tx.create(rel)

    parser = etree.XMLParser(dtd_validation=True, recover=True)
    tree = etree.parse(filename, parser)
    unicode_string = etree.tostring(tree.getroot(), encoding="unicode")
    catsoup = BeautifulSoup(unicode_string, "lxml-xml")

    cats = extract_information(catsoup, os.path.basename(filename))
    create_nodes_from_cats(cats, tx)


def read_index(filepath):
    element = {
        "personen": {
            "start": "listPerson",
            "element": "person",
            "method": extract_person_info,
        },
        "ortsregister": {
            "start": "listPlace",
            "element": "place",
            "method": extract_ortsregister,
        },
        "orgregister": {
            "start": "listOrg",
            "element": "org",
            "method": extract_orgregister,
        },
        "biblioregister": {
            "start": "listBibl",
            "element": "biblStruct",
            "method": extract_biblioregister,
        },
        "begriffsregister": {
            "start": "list",
            "element": "item",
            "method": extract_begriffsregister,
        },
        "artefaktenregister": {
            "start": "list",
            "element": "item",
            "method": extract_artefaktenregister,
        },
        "voelkerregister": {
            "start": "list",
            "element": "item",
            "method": extract_voelkerregister,
        },
    }
    parser = etree.XMLParser(dtd_validation=True, recover=True)
    tree = etree.parse(filepath, parser)
    unicode_string = etree.tostring(tree.getroot(), encoding="unicode")
    soup = BeautifulSoup(unicode_string, "lxml-xml")

    register = os.path.splitext(os.path.basename(filepath))[0]
    # find first element in register, e.g. named `listPerson` or `listBibl`
    starting_node = soup.find(element[register]["start"])

    infos = []
    # inside the list of register elements, only extract those we are interested in, e.g. `person` or `biblStruct`
    for child in starting_node.find_all(element[register]["element"]):
        info = element[register]["method"](child)
        infos.append(info)

    return infos


def extract_person_info(node):
    desired_info = {
        "_labels": ["person", "register"],
        "persName": "persName",
        "persName.surname": "surname",
        "birth.placeName.settlement": "birth:place",
        "birth:when": "birth:date",
        "birth": "birth:datestring",
        "death.placeName.settlement": "death:place",
        "death:when": "death:date",
        "death": "death:datestring",
    }
    info = {}
    extract_info(node, desired_info, info, "personen.xml")
    info["attrs"]["persName"] = " ".join(
        [
            info["attrs"].get(attr)
            for attr in ["persName", "surname"]
            if info["attrs"].get(attr)
        ]
    )
    return info


def extract_voelkerregister(node):
    desired_info = {"_labels": ["people", "register"], "term": ["peopleName"]}
    info = {}
    return extract_info(node, desired_info, info, "voelkerregister.xml")


def extract_artefaktenregister(node):
    desired_info = {
        "_labels": ["artefact", "register"],
        "name": ["artefactName"],
    }
    info = {}
    return extract_info(node, desired_info, info, "artefaktenregister.xml")


def extract_begriffsregister(node):
    desired_info = {
        "_labels": ["concept", "register"],
        "term": ["conceptName"],
    }
    info = {}
    return extract_info(node, desired_info, info, "begriffsregister.xml")


def extract_biblioregister(node):
    desired_info = {
        "_labels": ["bibliography", "register"],
        "title": "title",
        "author": {
            "_labels": ["bibliography", "author"],
            "persName.forename": "forename",
            "persName.surname": "surname",
            "persName": "persName",
            "orgName": "orgName",
        },
        "imprint": {
            "_labels": ["bibliography", "publisher"],
            "publisher": "publisher",
            "pubPlace": "pubPlace",
            "date": "date",
        },
    }
    info = {}
    return extract_info(node, desired_info, info, "biblioregister.xml")


def extract_orgregister(node):
    desired_info = {
        "_labels": ["organisation", "register"],
        "orgName": [],
        "location.country:key": "location:country",
        "location.settlement:type": "location:type",
        "location.settlement": "location:settlement",
    }
    info = {}
    return extract_info(node, desired_info, info, "orgregister.xml")


def extract_ortsregister(node):
    desired_info = {
        "_labels": ["place", "register"],
        "placeName": "placeName",
        "location.country:key": "country",
        "location.region": "region",
    }
    info = {}
    return extract_info(node, desired_info, info, "ortsregister.xml")


def extract_info(node, desired_info, info, filename=None):
    """extracts the information from the node and its children
    according to the desired information defined.
    Returns a dictionary.
    """
    info["labels"] = desired_info.get("_labels", node.name)
    info["attrs"] = node.attrs
    if filename and "xml:id" in node.attrs:
        info["attrs"]["xml:id"] = "#".join([filename, node.attrs["xml:id"]])

    texts = []
    for child in node.children:
        if child.name is None:
            node_text = child.strip()
            if node_text:
                texts.append(node_text)
    if texts:
        info["attrs"]["text"] = " ".join(texts)

    if desired_info:
        info["relations"] = []

    for element in desired_info:
        if element == "_labels":
            continue
        if isinstance(desired_info[element], list):
            # we have a number of terms
            terms = []
            for child_node in node.find_all(element):
                term = child_node.text
                if term:
                    terms.append(term)
            desired_info[element].append(element)
            label = desired_info[element][0]
            info["attrs"][label] = terms

        elif isinstance(desired_info[element], dict):
            # create a relation to a subnode
            for subnode in node.find_all(element):
                subinfo = {}
                extract_info(subnode, desired_info[element], subinfo)
                info["relations"].append(subinfo)

        else:
            # look for a value inside a nested node
            curr_node = node
            for el in element.split("."):
                node_name, attr, *_ = el.split(":") + [None]
                child_node = curr_node.find(node_name)
                if not child_node:
                    curr_node = None
                    break
                else:
                    curr_node = child_node

            if not curr_node:
                continue

            if desired_info[element].startswith(":"):
                # the value of an attribute sets the attribute name,
                # e.g. settlement:type
                # <settlement type="region">DE</settlement> --> region : DE
                attr_name = curr_node.attrs.get(desired_info[element][1:])
            else:
                attr_name = desired_info[element]

            if attr:
                # we asked for an attribute value, e.g. country:key   <country key="GB">
                value = curr_node.attrs.get(attr)
                if value:
                    info["attrs"][attr_name] = value
            else:
                # return the text within the opening and closing elements
                texts = []
                for child in curr_node.children:
                    if child.name:
                        continue
                    node_text = child.strip()
                    if node_text:
                        texts.append(node_text)
                if texts:
                    info["attrs"][attr_name] = " ".join(texts)

    return info


def find_child_instances_with_label(self, label):
    found = []
    for child_instance in self.child_instances:
        if label in child_instance.labels:
            found.append(child_instance)
        found += find_child_instances_with_label(child_instance, label)
    return found


def parse(filename, start_with_tag="TEI", idno=None, attrs=None, commit=None):
    status = defaultdict(list)
    status["attrs"] = defaultdict(dict)
    status["handshift"] = {}
    status["links"] = defaultdict(dict)
    if attrs is None:
        attrs = {}
    if commit is not None:
        attrs["commit_date"] = commit.committed_datetime.isoformat()
        attrs["commit_hash"] = commit.hexsha
        attrs["commit_message"] = commit.message
        attrs["creation_date"] = datetime.now().isoformat()

    filename_only = os.path.basename(filename)
    # attrs['filename'] = filename_only
    status["attrs"]["filename"] = filename_only

    # 1. parse the XML using lxml and etree.
    # It will apply the DTD validation and replace strings like &stern_1; with
    # the correct unicode symbol, which is described in the DTD file.
    parser = etree.XMLParser(dtd_validation=True, recover=True)
    tree = etree.parse(filename, parser)
    # output of XML document as unicode string
    unicode_string = etree.tostring(tree.getroot(), encoding="unicode")

    # 2. parse the TEI XML file (the unicode string), using lxml-xml parser
    # which is not assuming html and thus does not automatically add html or remove body tags.
    soup = BeautifulSoup(unicode_string, "lxml-xml")

    # find the primary key of the document and attach it to the soup
    if not idno:
        idno = soup.find("idno")
        if idno:
            idno = idno.string
        else:
            register_mapping = {
                "person": "personen.xml",
                "artefakt": "artefaktenregister.xml",
                "organisation": "orgregister.xml",
                "ort": "ortsregister.xml",
                "begriff": "begriffsregister.xml",
                "biblio": "biblioregister.xml",
                "volk": "voelkerregister.xml",
            }
            for k, v in register_mapping.items():
                if k in filename_only.lower():
                    start = filename_only.find("#")
                    end = filename_only.find(".xml")
                    if start and end:
                        idno = v + filename_only[start:end]
            if not idno:
                idno = filename_only[0:-4]

    status["attrs"]["idno"] = idno

    tei_node = soup.find(start_with_tag)
    if tei_node is None:
        raise ValueError(f"Did not find a tag named '{start_with_tag}'")

    # find a matching class, create an object from it
    # and return it
    class_name = start_with_tag.lower()
    if class_name in globals():
        cls = globals()[class_name]
        doc = cls(node=tei_node, node_name=tei_node.name, status=status, attrs=attrs)
        return doc, status, tei_node
    else:
        raise ValueError(f"no such class available: {class_name}")


# TEI section
class tei:
    """This is the base class for all elements in a TEI document."""

    def __init_subclass__(
        cls,
        parent_child_relation="CONTAINS",
        child_parent_relation=None,
        collect_text=False,
        do_not_store_this_node=False,
        add_label_to_children=None,
        unpack_elements=False,
        create_auxiliary_node=False,
        create_empty_token_nodes=False,
        from_relation_attr=None,
        to_relation_attr=None,
        group_similar_siblings=None,
        pass_attributes_to_children=False,
        cache_object=False,
        **kwargs,
    ):
        super().__init_subclass__(**kwargs)
        # Parent defines,  how the relation from Parent to Child is defined
        cls.parent_child_relation = parent_child_relation
        # Child defines, how the relation from Child to Parent is defined
        cls.child_parent_relation = child_parent_relation
        cls.collect_text = collect_text  # extract all text inside this element, store it into the `string` attribute
        # ignore this element (do not add an additional node), just add the elements inside it
        cls.unpack_elements = unpack_elements
        # add additional node with relation to the token (e.g. the ref element)
        cls.create_auxiliary_node = create_auxiliary_node
        # if an empty <sic/> element is encountered, create a token node
        # even the element contains no tokens at all
        cls.create_empty_token_nodes = (
            create_empty_token_nodes  # create additional nodes that contain whitespace
        )
        cls.from_relation_attr = from_relation_attr
        cls.to_relation_attr = to_relation_attr
        cls.group_similar_siblings = group_similar_siblings  # see
        cls.add_label_to_children = (
            add_label_to_children  # add additional label to node
        )
        cls.pass_attributes_to_children = (
            pass_attributes_to_children  # add attributes of xml-node to graph-node
        )
        cls.cache_object = cache_object
        cls.do_not_store_this_node = do_not_store_this_node

    def get_class_for_node(self, node):
        # add an underscore to the node name in case it is a reserved python word
        # which can't be used as a class name
        node_name = node.name
        if node_name in keyword.kwlist:
            node_name += "_"

        # inspect all subclasses in a class (and their parents)
        # and try to find a matching class to the given
        # node_name (aka tag, element) in the XML file
        # return the class as soon as it is found, using
        # C3 mro (method resolution order)

        for cls in inspect.getmro(self.__class__):
            if cls.__name__ == "object":
                continue

            for subclass_tuple in inspect.getmembers(
                cls, predicate=lambda cl: (inspect.isclass(cl))
            ):
                if node_name.lower() == subclass_tuple[0].lower():
                    return subclass_tuple[1]

        # still no matching class found.
        # Try to find a base class (has lower precedence than a specialized class)
        if node_name.lower() in globals():
            return globals()[node_name.lower()]
        else:
            return None

    def handle_whitespace(self, *_):
        return []

    def parse_string(self, node, status, parent_attrs, parent_labels):
        """Gets the string  within an opening and a closing tag:
        <title>some string</title>
        ... and stores it as an attribute: object.string
        This method can be overriden to parse the string and create
        individual token objects instead.
        returns an array containing the object
        """
        # either get the string directly found in the tag
        # or within all children
        string = getattr(node, "string", "") or getattr(node, "text", "")
        # remove all leading and trailing whitespace
        self.attrs["string"] = string.strip()

    def parse_comment(self, node, status):
        comment_instance = comment(node=node, node_name=node.name, status=status)
        return [comment_instance]

    def _change_base_class(self):
        """During object initialization we will change the parents (base classes)
        of the object dynamically.
        Nested classes like A.B.C do not inherit from each other and there is no way
        to make it work:

        class A(tei):
            class B(A, tei):
                class C(B, A, special_class, tei):
                    ...

        Will already fail on compile time.

        To make an object inherit from the classes it is nested in, we need to change
        its base classes, i.e. object.__class__.__bases__. This can be achieved on
        runtime.

        So if we declare our classes like this:

        class A(tei):
            class B(tei):
                class C(special_class, tei):
                    pass

        the resulting objects will behave as if the classes were defined like this:

        class A(tei):
            class B(A, tei)
                class C(special_class, A.B, A, tei)


        Why would we want to have nested classes? Isn't this bad practice?
        ------------------------------------------------------------------

        When parsing a TEI document, we do not treat similar elements
        always the same way.
        For example, a paragraph element <p> can occur almost everywhere
        inside the <text> or <body> elements.
        It also appears in the <teiHeader>, but there its content
        needs to be treated differently. We could define a general class p which has
        a lot of ifs to decide how to behave in which situation. To avoid this, we
        rather define a class

            text.body.p

        which is a completely different class than

            teiheader.p

        At the same time, we want text.body.p to use some of the specialised methods
        defined in the class text.body, for example.

        The resulting code will be declarative, easy to read and maintain.

        """
        # ------------ start changing base class of object --------------
        # get the qualified name of our class without the module name,
        # e.g. 'A.B.C', not '__main__.A.B.C' and not just 'A'
        # NOTE: only works with Python 3.3 and onwards!
        fqn = self.__class__.__qualname__
        class_names = fqn.split(".")

        # get the list of classes we already inherit from
        result_classes = list(self.__class__.__bases__)

        # from the fully qualified class (e.g. A.B.C) we want the given class to
        # inherit from A.B, A (in this order). We put this classes in front of
        # the already present classes (thus insert not append)
        for i in range(1, len(class_names)):
            cls_name = ".".join(class_names[0:i])
            try:
                cls = eval(cls_name)
                if cls not in result_classes:
                    result_classes.insert(0, cls)
            except AttributeError:
                # class is not explicitly defined (only as virtual metaclass)
                pass

        # change the __class__.__bases__ of our newly created object
        # which now is of Classes A.B.C, A.B, A and any other classes it inherits
        self.__class__.__bases__ = tuple(result_classes)
        # ------------ finish changing base class of object --------------

    def __init__(
        self,
        node=None,
        node_name=None,
        status=None,
        attrs=None,
        parent_attrs=None,
        parent_labels=None,
    ):
        """tei class is the parent class for all tei elements.
        node: the current node in the tei-xml file
        node_name: name of the current element (e.g. p, lb, teiheader)
        status: during parsing, certain events like handShift needs to be registered
              these events affect all next elements
        attrs: attributes inside an element
        parent_attrs: attributes that are passed to all children elements
            Attributes of children might overwrite them again, much like in css.
        string: the actual value (or payload) of an element. Header information
            is not getting interpreted any further, whereas the text itself
            is interpreted (by the parse_string function)
        parent_labels: labels that are passed to all children elements,
            much like parent_attrs.

        """

        # make nested classes inherit from each other
        # by dynamically changing their base classes
        self._change_base_class()

        # the node of the xml parser
        self.xml_node = node

        # set the name of the node, in case it was not provided
        if node_name is None:
            setattr(self, "node_name", self.__class__.__name__)
        else:
            setattr(self, "node_name", node_name)

        # add the name of the node as the default label
        self.labels = set()
        self.labels.add(node_name)

        self.child_parent_relation = None

        # If there are any parent attributes, merge them into
        # the attributes of the current child object.
        # make sure the parent attributes are overwritten if a child
        # has the same attributes.
        self.attrs = defaultdict()
        if attrs is None:
            attrs = {}
        if parent_attrs is None:
            parent_attrs = {}
        self.attrs = {**self.attrs, **parent_attrs, **attrs}

        # collect all the attributes we stored in self.attrs
        # and merge them with node attributes
        node_attrs = getattr(node, "attrs", {})
        for k, v in node_attrs.items():
            # in some cases, attributes are not of class str but bs4.element.NamespacedAttribute
            self.attrs[str(k)] = v

        # collect all attributes we stored in status['attrs']
        # including the primary key (idno) of the document
        if status is not None:
            for key in status["attrs"]:
                self.attrs[key] = status["attrs"][key]

        if parent_labels is None:
            parent_labels = []

        # add delSpan label if we have such a status
        if status.get("delSpan"):
            self.labels.add("delSpan")
            # add delSpan attribute with anchor id
            self.attrs["delSpan"] = status.get("delSpan")

        # add any incoming parent labels to self.labels
        # and make a copy into new_parent_labels
        new_parent_labels = []
        for parent_label in parent_labels:
            self.labels.add(parent_label)
            new_parent_labels.append(parent_label)

        # new_parent_labels now contains all the labels that need to be
        # passed to all children objects
        if getattr(self, "add_label_to_children", False):
            new_parent_labels.append(self.add_label_to_children)

        self.child_instances = []

        # Parse the string of the element itself
        if getattr(self, "collect_text", False):
            # the node class gets this attribute,
            # extract all the node's text and store it into the `string` attribute
            self.parse_string(node, status, parent_attrs, parent_labels)

        if node is None or node.name is None:
            # we encountered just text, which has no node.name and no children either.
            pass
        else:
            # Walk through children of the current node
            new_parent_attrs = {}
            if getattr(self, "pass_attributes_to_children", False):
                new_parent_attrs = self._get_node_attributes()
                # do not inherit xml:id attribute to children
                if "xml:id" in new_parent_attrs:
                    new_parent_attrs.pop("xml:id")
            new_parent_attrs = {**parent_attrs, **new_parent_attrs}

            for child_node in node.children:
                # - walk through the children of the current node
                # - find a corresponding class, either directly or indirectly
                # - create an instance of it
                # - append the child_instances to the object.child_instances attribute

                if child_node.isspace is not None and child_node.isspace():
                    # we did not find any characters, just whitespace
                    child_instances = self.handle_whitespace(
                        child_node, status, new_parent_attrs, new_parent_labels
                    )
                    self.child_instances += child_instances
                    continue

                elif child_node.name is None:
                    # we encountered TEXT or COMMENT, which is not enclosed in tags
                    # but occurs after a tag (e.g. after a linebreak <lb>)
                    if isinstance(child_node, Comment):
                        # COMMENT
                        continue
                        # self.child_instances += self.parse_comment(child_node, status)
                    elif not getattr(self, "collect_text", False):
                        # Unless we have not already collected the text in all sub-elements:
                        # we need to parse the TEXT, which means:
                        # we tokenize it and create token objects
                        child_instances = self.parse_string(
                            child_node, status, new_parent_attrs, new_parent_labels
                        )
                        if child_instances is not None:
                            self.child_instances += child_instances

                else:
                    # we encountered an child-node (child-element)
                    # find class for child_node
                    targetClass = self.get_class_for_node(child_node)

                    # if we do not find a matching class,
                    # we will ignore the entire element and all its children
                    if targetClass is None:
                        continue
                    else:
                        # we found a matching class: create an instance of it and
                        # append it to self.child_instances
                        instance = targetClass(
                            node=child_node,
                            node_name=child_node.name,
                            status=status,
                            parent_attrs=new_parent_attrs,
                            parent_labels=new_parent_labels,
                        )

                        # a class implements the parse_attrs method
                        # e.g. unclear, which will create an additional token-node
                        if getattr(instance, "parse_attrs", False):
                            instance.parse_attrs()

                        # if class has the attribute unpack_elements=True
                        # we want to directly append the children of the children
                        # to the current instance.
                        if instance.unpack_elements:
                            if (
                                instance.create_empty_token_nodes
                                and len(instance.child_instances) == 0
                            ):
                                token_obj = Token(
                                    node=child_node,
                                    node_name="token",
                                    status=status,
                                    attrs={"string": "", "whitespace": ""},
                                    parent_labels=new_parent_labels
                                    + [instance.node_name],
                                )
                                self.child_instances.append(token_obj)

                            if getattr(instance, "parse_attrs", False):
                                instance.parse_attrs()

                            if (
                                instance.create_auxiliary_node
                                and instance.child_instances
                            ):
                                # Create an additional node with relations to first and last token
                                instance.child_instances[0].relationships.append(
                                    {
                                        "from": instance,
                                        "to": instance.child_instances[0],
                                        "label": instance.__class__.__name__ + "_START",
                                    }
                                )
                                instance.child_instances[-1].relationships.append(
                                    {
                                        "from": instance,
                                        "to": instance.child_instances[-1],
                                        "label": instance.__class__.__name__ + "_END",
                                    }
                                )
                            for child_instance in instance.child_instances:
                                self.child_instances.append(child_instance)
                            if getattr(instance, "create_auxiliary_node", False):
                                # if we need to create an auxiliary node,
                                # we have to add it here to the children
                                # (we will ignore it later again when connecting the siblings)
                                self.child_instances.append(instance)
                        else:
                            self.child_instances.append(instance)

        self.create_parent_child_relationships()
        self._group_similar_siblings()

    def _get_node_attributes(self):
        """returns all attributes of an XML element as a dict"""
        attrs = {}
        for attr in self.xml_node.attrs:
            attrs[attr] = self.xml_node.attrs[attr]
        return attrs

    def create_parent_child_relationships(self):
        """This is the default relation between parent and child objects: CONTAINS
        Certain classes (like p) might implement their own, specific relations.
        If you just want to override the default, add

            class myclass(tei, parent_child_relation='WHATEVER')

        to your class definition.

        If you would like to break the hierarchical order of the elements
        and chain the nodes instead, use the ConnectSiblings class which
        overrides this method.
        """
        self.relationships = []
        label = getattr(self, "parent_child_relation", "CONTAINS")
        for child_instance in self.child_instances:
            if getattr(self, "create_auxiliary_node", False):
                return
            self.relationships.append(
                {
                    "from": self,
                    "to": child_instance,
                    "label": label,
                }
            )

    def _group_similar_siblings(self):
        """Creates additional relationships between similar siblings
        e.g. NEXT_LB, NEXT_TOKEN
        Also creates relationships that point to the first and last element:
        FIRST_LB, LAST_LB
        Classes must be declared this way:
        class body(tei, group_similar_siblings=['p'])
        """
        if getattr(self, "group_similar_siblings", None) is None:
            return

        prev_instance = {}
        counter = defaultdict(int)
        for instance in [
            child_instance
            for child_instance in self.child_instances
            if child_instance.node_name in self.group_similar_siblings
        ]:
            counter[instance.node_name] += 1
            # FIRST appearance
            if counter[instance.node_name] == 1:
                self.relationships.append(
                    {
                        "from": self,
                        "to": instance,
                        "label": "FIRST_" + instance.node_name.upper(),
                    }
                )

            if prev_instance.get(instance.node_name):
                self.relationships.append(
                    {
                        "from": prev_instance[instance.node_name],
                        "to": instance,
                        "label": "NEXT_" + instance.node_name.upper(),
                    }
                )

            prev_instance[instance.node_name] = instance

        # LAST
        for node_name in self.group_similar_siblings:
            if prev_instance.get(node_name):
                self.relationships.append(
                    {
                        "from": self,
                        "to": prev_instance[node_name],
                        "label": "LAST_" + node_name.upper(),
                    }
                )

    def _update_node(self, node, labels, attrs):
        for label in labels:
            node.add_label(label)
        for attr in attrs:
            node[attr] = attrs[attr]

    def _node_for_obj(self, obj, tx, node_cache):
        """This method creates graph nodes for a given object."""
        attrs = getattr(obj, "attrs", {})

        if not getattr(obj, "node", False):
            labels = list(obj.labels)

            # if we got a node with an xml:id we first want to check whether we
            # already have an empty node to update
            xml_id = attrs.get("xml:id")
            filename = attrs.get("filename")
            if xml_id and filename:
                node = None
                if filename in node_cache and xml_id in node_cache[filename]:
                    # search in cache
                    node = node_cache[filename][xml_id]
                    self._update_node(node, labels, attrs)
                else:
                    # create node, make sure bs4.element.NavigableString items are strings
                    safe_attrs = {}
                    for k, v in attrs.items():
                        safe_attrs[str(k)] = str(v)
                    node = Node(
                        *labels,
                        **safe_attrs,
                    )

                    # store node in node_cache
                    if filename not in node_cache:
                        node_cache[filename] = {}
                    node_cache[filename][xml_id] = node

            # we do not have a node with xml:id attribute
            else:
                # create node, make sure bs4.element.NavigableString items are strings
                safe_attrs = {}
                for k, v in attrs.items():
                    safe_attrs[str(k)] = str(v)
                node = Node(
                    *labels,
                    **safe_attrs,
                )
                tx.create(node)
            obj.node = node
        return obj.node

    def save(self, tx, node_cache=None):
        """Recursively walk through all child_instances generated and
        create nodes and relationships in the graph database
        """
        if node_cache is None:
            node_cache = {}

        # create node for the current element
        # adding element attributes, e.g. <p attr1="one" attr2="two">
        # as attributes to the node itself

        # create all nodes (if they do not exist yet) and relationships
        for relationship in self.relationships:
            from_node = self._node_for_obj(relationship["from"], tx, node_cache)
            to_node = self._node_for_obj(relationship["to"], tx, node_cache)
            attr = relationship.get("attr", {})
            rel = Relationship(from_node, relationship["label"], to_node, **attr)
            tx.create(rel)

        for child_instance in self.child_instances:
            child_instance.save(tx, node_cache)


class include_all_children:
    def get_class_for_node(self, node):
        """Inside a given section we want to follow every child element,
        even the ones we have no class definition for.
        We therefore have to instantly create new child classes using type()
        """
        cls = super().get_class_for_node(node)
        if cls is None and node.name is not None:
            node_name = node.name

            parent_classes = [parent.name for parent in node.parents][:-2]
            parent_classes.reverse()
            parent_classes.append(node_name)

            # add an underscore to the class name
            # in case it is a reserved python word
            # --> reserved python words cannot be used as a class name
            for i, class_name in enumerate(parent_classes):
                if class_name in keyword.kwlist:
                    parent_classes[i] = class_name + "_"

            class_name = ".".join(parent_classes)
            class_name = class_name.lower()

            return type(class_name, (tei, object), {})
        else:
            return cls


class ParseString(include_all_children, tei):
    def parse_string(self, node, status, parent_attrs, parent_labels):
        """This method parses the string between elements by dividing
        it into Token objects, using spacy.io
        returns: all token objects as an a array of objects
        """

        if getattr(self, "collect_text", False):
            # only collect the text in the first iteration, when we iterate
            # over all sub-elements
            if not self.attrs.get("string"):
                string = getattr(node, "string", "") or getattr(node, "text", "")
                # remove all leading and trailing whitespace
                self.attrs["string"] = string.strip()

        line = getattr(node, "string", "")
        if line is None:
            return []

        line = str(line)

        # remove newlines and whitespace / tabs that are after a newline,
        # since they belong to XML formatting, not to actual wanted text

        # FIXME: we need to make sure we do not accidentally introduce new spaces
        line = re.sub(r"[\n\r]+([\t\s]*)", " ", line, flags=re.MULTILINE)

        # we did not see anything other than tabs, newlines and whitespace
        if line == "" or re.search(r"^\s+$", line):
            return []

        # finally do the tokenization using spacy's nlp
        tokens = nlp(line)

        token_objs = []
        # Walk through text-tokens and create Token objects
        for token in tokens:
            ends_with_hyphen = False
            if any(
                token.text.endswith(s)
                for s in ["-", "\N{NOT SIGN}", "\N{NON-BREAKING HYPHEN}"]
            ):
                ends_with_hyphen = True

            attrs = {
                "is_punct": token.is_punct,
                "pos": token.pos_,
                "tag": token.tag_,
                "ends_with_hyphen": ends_with_hyphen,
                "string": token.text,
                "whitespace": token.whitespace_,  # token is followed by a whitespace
                # from handshift:
                "medium": status.get("handshift").get("medium"),
                "script": status.get("handshift").get("script"),
            }
            if any(
                token.text.endswith(s)
                for s in ["-", "\N{NOT SIGN}", "\N{NON-BREAKING HYPHEN}"]
            ):
                attrs["is_hyphened"] = True

            # Merge parent_attrs into attrs
            # but let them to be overwritten by the child elements
            if parent_attrs:
                attrs = {**parent_attrs, **attrs}

            # Create a Token object for every token
            token_obj = Token(
                node=node,
                node_name="token",
                status=status,
                attrs=attrs,
                parent_labels=parent_labels,
            )

            # add it to our collection of token objects
            token_objs.append(token_obj)

        # these token objects get appended to .child_instances
        return token_objs

    handle_whitespace = parse_string


class ConnectSiblings:
    """This class defines how siblings, i.e. elements on the same hierarchical level,
    are connected with
    - each other
    - between the parent and the first and last children

    Default:
    parent-FIRST->sibling-NEXT->sibling<-LAST-parent

    Classes that inherit from this class can define attributes (see below)
    to define specific behaviour.
    """

    def __init_subclass__(
        cls,
        parent_to_first_sibling_relation="FIRST",
        first_sibling_to_parent_relation=None,
        parent_to_last_sibling_relation="LAST",
        last_sibling_to_parent_relation=None,
        previous_next_sibling_relation="NEXT",
        previous_next_relation_attr=None,
        next_previous_sibling_relation=None,
        next_previous_relation_attr=None,
        create_additional_parent_child_relations=None,
        **kwargs,
    ):
        super().__init_subclass__(**kwargs)
        cls.parent_to_first_sibling_relation = parent_to_first_sibling_relation
        cls.parent_to_last_sibling_relation = parent_to_last_sibling_relation
        cls.last_sibling_to_parent_relation = last_sibling_to_parent_relation
        cls.first_sibling_to_parent_relation = first_sibling_to_parent_relation

        cls.previous_next_sibling_relation = previous_next_sibling_relation
        if previous_next_relation_attr is None:
            previous_next_relation_attr = {}
        cls.previous_next_relation_attr = previous_next_relation_attr

        cls.next_previous_sibling_relation = next_previous_sibling_relation
        if next_previous_relation_attr is None:
            next_previous_relation_attr = {}
        cls.next_previous_relation_attr = next_previous_relation_attr
        cls.create_additional_parent_child_relations = (
            create_additional_parent_child_relations
        )

    def create_parent_child_relationships(self):
        """Replaces the usual parent-child relationships (CONTAINS) from the tei class,
        by chaining the siblings and pointing from the parent to the FIRST sibling,
        then connecting to the NEXT sibling
        and finally pointing from the parent to the LAST sibling
        """
        prev_child_instance = None
        self.relationships = []

        # skip child instances that will not be stored
        child_instances = list(
            child for child in self.child_instances if not child.do_not_store_this_node
        )

        if self.create_additional_parent_child_relations:
            for (
                label,
                relation,
            ) in self.create_additional_parent_child_relations.items():
                for child_instance in find_child_instances_with_label(self, label):
                    self.relationships.append(
                        {
                            "from": self,
                            "to": child_instance,
                            "label": relation,
                        }
                    )

        for i, child_instance in enumerate(child_instances):
            if getattr(child_instance, "create_auxiliary_node", False):
                # auxiliary nodes should not be part of a sibling-chain
                continue
            if getattr(self, "create_auxiliary_node", False):
                # auxiliary nodes should not establish a standard parent-child connection
                # instead: e.g. rs_START and rs_END
                continue
            # First sibling
            if i == 0:
                if self.parent_to_first_sibling_relation:
                    self.relationships.append(
                        {
                            "from": self,
                            "to": child_instance,
                            "label": self.parent_to_first_sibling_relation,
                        }
                    )
                if self.first_sibling_to_parent_relation:
                    self.relationships.append(
                        {
                            "from": child_instance,
                            "to": self,
                            "label": self.first_sibling_to_parent_relation,
                        }
                    )

            if prev_child_instance is not None:
                if self.previous_next_sibling_relation:
                    self.relationships.append(
                        {
                            "from": prev_child_instance,
                            "to": child_instance,
                            "label": self.previous_next_sibling_relation,
                            "attr": self.previous_next_relation_attr,
                        }
                    )
                if self.next_previous_sibling_relation:
                    self.relationships.append(
                        {
                            "from": child_instance,
                            "to": prev_child_instance,
                            "label": self.next_previous_sibling_relation,
                            "attr": self.next_previous_relation_attr,
                        }
                    )

            # last sibling
            if i == len(child_instances) - 1:
                if self.parent_to_last_sibling_relation:
                    self.relationships.append(
                        {
                            "from": self,
                            "to": child_instance,
                            "label": self.parent_to_last_sibling_relation,
                        }
                    )
                if self.last_sibling_to_parent_relation:
                    self.relationships.append(
                        {
                            "from": child_instance,
                            "to": self,
                            "label": self.last_sibling_to_parent_relation,
                        }
                    )
            prev_child_instance = child_instance


class teiheader(tei):
    """teiHeader section
    only the elements listed here are being parsed and
    added to the database. Strings in an element are,
    as opposed to the BODY section, not being tokenized
    (split into words etc.)."""

    class filedesc(include_all_children, tei):
        pass

    class physdesc(tei):
        class handdesc(tei):
            """collect_text=True makes all text within the handDesc element
            to be parsed like text"""

            class summary(tei, collect_text=True):
                pass

            class handnote(
                # tei class needs to be _after_ ConnectSiblings,
                # so the paragraph tokens get chained
                ConnectSiblings,
                tei,
                collect_text=True,
                create_additional_parent_child_relations={
                    "locus": "has_locus",
                    "rs": "has_rs",
                },
            ):
                class p(
                    ParseString,
                    ConnectSiblings,
                ):
                    class locus(
                        ParseString,
                        unpack_elements=True,
                        create_auxiliary_node=True,
                    ):
                        pass

        # class objectdesc(tei):
        class objectdesc(tei):
            class supportdesc(tei):
                class support(tei, collect_text=True):
                    pass

                class foliation(
                    ParseString,
                    ConnectSiblings,
                    tei,
                    collect_text=True,
                ):
                    pass

                class collation(tei, collect_text=True):
                    pass

                class condition(tei, collect_text=True):
                    pass

                class extent(tei, collect_text=True):
                    pass

    class msidentifier(include_all_children, tei):
        pass

    class encodingdesc(tei):
        class editorialdecl(tei, collect_text=True):
            pass

    class profiledesc(include_all_children, tei):
        pass

    class revisiondesc(include_all_children, tei):
        pass


# FACSIMILE section
# the facsimilies section defines zones (coordinates) on the image itself
# every zone contains an xml:id which is used in paragraphs to refer to: <p facs="#facs_1_r3">
class facsimile(tei, cache_object=True):
    class surface(tei):
        class graphic(tei):
            pass

        class zone(tei, cache_object=True):
            pass


# TEXT section
# <text> is actually holding the real content in every TEI document
class text(include_all_children, tei):
    def get_class_for_node(self, node):
        """Inside the <text> section we want to follow every element,
        even the ones we have no class definition for.
        We therefore have to instantly create a new class using type()
        """
        cls = super().get_class_for_node(node)
        if cls is None and node.name is not None:
            node_name = node.name

            parent_classes = [parent.name for parent in node.parents][:-2]
            parent_classes.reverse()
            parent_classes.append(node_name)

            # add an underscore to the class name
            # in case it is a reserved python word
            # --> reserved python words cannot be used as a class name
            for i, class_name in enumerate(parent_classes):
                if class_name in keyword.kwlist:
                    parent_classes[i] = class_name + "_"

            class_name = ".".join(parent_classes)

            return type(class_name, (tei, object), {})
        else:
            return cls

    class front(tei):
        pass

    class body(
        ConnectSiblings,
        tei,
        parent_to_first_sibling_relation="FIRST_ELEMENT",
        previous_next_sibling_relation="NEXT_ELEMENT",
    ):
        class p(
            ParseString,  # parse string, split into tokens
            ConnectSiblings,
            group_similar_siblings=["lb"],
            parent_to_first_sibling_relation="NEXT",
            parent_to_last_sibling_relation="LAST",
            previous_next_sibling_relation="NEXT",
        ):
            """handles all paragraphs tags <p> within the <body> tag"""

            def __init__(
                self,
                node=None,
                node_name=None,
                status=None,
                parent_attrs=None,
                parent_labels=None,
            ):
                # add paragraph_id to status attrs,
                # as we add the paragraph_id to all nodes
                if node.get("xml:id"):
                    status["attrs"]["paragraph_id"] = node.get("xml:id")
                super().__init__(
                    node=node,
                    node_name=node_name,
                    status=status,
                    parent_attrs=parent_attrs,
                    parent_labels=parent_labels,
                )
                # remove paragraph_id again when we leave
                # this paragraph
                if "paragraph_id" in status["attrs"]:
                    status["attrs"].pop("paragraph_id")

        class pb(ParseString):
            pass

        class fw(ParseString):
            pass

        class undo(ParseString):
            pass

    class back(ParseString):
        pass


class comment(tei):
    pass


class Token(
    ConnectSiblings,
    tei,
):
    pass


class Word(
    ConnectSiblings,
    tei,
):
    pass


class handshift(tei, do_not_store_this_node=True):
    def __init__(
        self,
        node=None,
        node_name=None,
        status=None,
        attrs=None,
        parent_attrs=None,
        parent_labels=None,
    ):
        # only overwrite the latest handshifts, keep everything else.
        if node.get("new"):
            status["handshift"]["new"] = node.get("new")
        if node.get("medium"):
            status["handshift"]["medium"] = node.get("medium")
        if node.get("script"):
            status["handshift"]["script"] = node.get("script")

        super().__init__(node=node, node_name=node_name, status=status)


class delspan(tei):
    """a delSpan element marks all following elements to be deleted,
    until an anchor element appears that contains the ID of the spanTo attribute.
    Albeit currently not needed, we still store this node in the graph.
    """

    def __init__(
        self,
        node=None,
        node_name=None,
        status=None,
        attrs=None,
        parent_attrs=None,
        parent_labels=None,
    ):
        if node.get("spanTo"):
            spanTo = node.get("spanTo")
            # find first occurence of the anchor tag #
            # and store this
            spanTo = spanTo[spanTo.find("#") + 1 :]
            status["delSpan"] = spanTo

        super().__init__(node=node, node_name=node_name, status=status)


class anchor(tei):
    """a delSpan element always points to an anchor object. Because of this, we need
    to alter the status back to normal when we encounter an anchor object.
    """

    def __init__(
        self,
        node=None,
        node_name=None,
        status=None,
        attrs=None,
        parent_attrs=None,
        parent_labels=None,
    ):
        if status.get("delSpan"):
            if status.get("delSpan") == node.get("xml:id"):
                status.pop("delSpan")

        super().__init__(node=node, node_name=node_name, status=status)


class rs(
    ParseString,
    unpack_elements=True,
    create_auxiliary_node=True,
):
    """Reference String
    see https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-rs.html
    This will create an addtional node which the contained token nodes point to.
    """


class unclear(
    ParseString,
    unpack_elements=True,
    add_label_to_children="unclear",
    pass_attributes_to_children=True,
):
    """Elements <unclear> act like normal tokens
    even if they contain no character at all. Which means, the `token` label is being added.
    The `unclear` label will be passed to all contained nodes.
    If the attribute `extent` is present, a pseudo-string with ¿
    for every «Graphen» will be inserted.
    """

    def parse_attrs(self):
        """handles the extent attribute, i.e. adds an additional string:
        extent="3 Graphen" --> ¿¿¿
        """

        labels = list(self.labels)
        labels.append("token")
        self.labels = set(labels)
        if "extent" in self.attrs:
            match = re.search(
                r"(?P<number_of_graphs>\d+)\s+Graph", self.attrs["extent"]
            )
            if match:
                string = ""
                try:
                    string = "¿" * int(match.groupdict()["number_of_graphs"])
                    self.attrs["string"] = string
                    self.attrs["whitespace"] = ""
                except Exception:
                    pass
        else:
            self.attrs["string"] = ""
            self.attrs["whitespace"] = ""


class add(
    ParseString,
    unpack_elements=True,
    add_label_to_children="add",
    pass_attributes_to_children=True,
):
    """During parsing, this class should add the label "add"
    to every child element and all attributes should be passed to its children.
    """


class del_(
    ParseString,
    unpack_elements=True,
    add_label_to_children="del",
    pass_attributes_to_children=True,
):
    """During parsing, this class should add the label "del"
    to every child element and all attributes should be passed to its children.
    """


class subst(
    ParseString,
    unpack_elements=True,
    add_label_to_children="subst",
    pass_attributes_to_children=True,
):
    """
    Substitutions add some interpretation to the text,
    e.g. they suggest that a correction is done in one
    single pass. The del and add elements inside a subst
    are therefore grouped together.
    """


class metamark(
    ParseString,
    unpack_elements=True,
    add_label_to_children="metamark",
    pass_attributes_to_children=True,
):
    pass


class hi(
    ParseString,
    unpack_elements=True,
    add_label_to_children="hi",
    pass_attributes_to_children=True,
):
    pass


class quote(
    ParseString,
    unpack_elements=True,
    add_label_to_children="quote",
    pass_attributes_to_children=True,
):
    pass


class app(tei):
    class note(include_all_children, tei):
        pass


class note(
    ParseString,
    unpack_elements=True,
    add_label_to_children="note",
    pass_attributes_to_children=True,
):
    pass


class sic(
    ParseString,
    unpack_elements=True,
    add_label_to_children="sic",
    create_empty_token_nodes=True,
    pass_attributes_to_children=True,
):
    pass


class corr(
    ParseString,
    unpack_elements=True,
    add_label_to_children="corr",
    pass_attributes_to_children=True,
):
    pass


class choice(
    ParseString,
    unpack_elements=True,
    add_label_to_children="choice",
):
    pass

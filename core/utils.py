# BEGIN IMPORTS
from __future__ import print_function
import xml.etree.ElementTree
from collections import defaultdict
# END IMPORTS

  
  
class XmlConverter(object):
    '''XML methods:
    plain_to_etree(plain) : formats: plain text -> etree
    plain_to_dict(plain)  : formats: plain      -> dict
    etree_to_dict(etree)  : formats: etree      -> dict
    '''
    def __init__(self):
      super(self.__class__, self).__init__()
    
    @classmethod
    def plain_to_etree(self,plain):
        '''formats plain text -> etree'''
        self.t=xml.etree.ElementTree.XML(plain)
        
    @classmethod
    def plain_to_dict(self,plain):
        '''fomrats plain to dict'''
        return self.etree_to_dict(xml.etree.ElementTree.XML(plain))
      
    @classmethod  
    def etree_to_dict(self,t):
        '''formats etree -> dict'''
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self.etree_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def subdict(adict,keys):
    """
    Returns a subset of a dict
    """
    return dict((k,adict[k]) for k in keys if k in adict)
  
  
if __name__ == '__main__':
    print("nothing to do here")
    print(XmlConverter.__doc__)

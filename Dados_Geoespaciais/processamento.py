import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom 

def carregar_arquivo(caminho):
    if caminho.endswith(".csv"):
        return pd.read_csv(caminho)
    elif caminho.endswith(".json"):
        return pd.read_json(caminho)
    elif caminho.endswith(".xml"):
        return carregar_xml(caminho)
    else:
        raise ValueError("Formato não suportado. Use CSV, JSON ou XML.")

def carregar_xml(caminho):
    tree = ET.parse(caminho)
    root = tree.getroot()
    dados = []

    items_to_check = root.findall(".//registro") if root.tag == "dados" else root.findall("registro")
    if not items_to_check and root.tag != "registro": 
         items_to_check = root.findall("registro")
    if not items_to_check and root.tag == "registro": 
        items_to_check = [root]


    for item in items_to_check:
        dados.append({
            "nome": item.findtext("nome"),
            "latitude": float(item.findtext("latitude")),
            "longitude": float(item.findtext("longitude")),
        })
    return pd.DataFrame(dados)

def _pretty_print_xml(elem):
    """Retorna uma string XML formatada (indentada)."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def salvar_arquivo(df, caminho):
    if caminho.endswith(".csv"):
        df.to_csv(caminho, index=False)
    elif caminho.endswith(".json"):
        df.to_json(caminho, orient="records", indent=2)
    elif caminho.endswith(".xml"):
        root_element = ET.Element("dados") 
        for _, row in df.iterrows():
            registro_element = ET.SubElement(root_element, "registro")
            nome_element = ET.SubElement(registro_element, "nome")
            nome_element.text = str(row["nome"])
            lat_element = ET.SubElement(registro_element, "latitude")
            lat_element.text = str(row["latitude"])
            lon_element = ET.SubElement(registro_element, "longitude")
            lon_element.text = str(row["longitude"])
        
        xml_str = _pretty_print_xml(root_element)
        
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(xml_str)
            
    else:
        raise ValueError("Formato de salvamento não suportado. Use CSV, JSON ou XML.")
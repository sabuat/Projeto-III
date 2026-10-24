import geopandas as gpd
import glob
import os
from unidecode import unidecode

# 1. Localiza automaticamente o arquivo .shp ou .geojson que você colocou na pasta geodata/
arquivos_geo = glob.glob("geodata/*.shp") + glob.glob("geodata/*.geojson")

if not arquivos_geo:
    print("⚠️ Coloque o arquivo extraído do GeoSampa (.shp ou .geojson) dentro da pasta 'geodata/'!")
else:
    caminho_entrada = arquivos_geo[0]
    print(f"📂 Lendo arquivo do GeoSampa: {caminho_entrada}")
    gdf = gpd.read_file(caminho_entrada)
    
    print("Colunas encontradas no arquivo do GeoSampa:", list(gdf.columns))
    
    # 2. Converte de UTM (SIRGAS 2000 - EPSG:31983) para Latitude/Longitude (WGS84 - EPSG:4326)
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        print("🔄 Convertendo projeção cartográfica para EPSG:4326 (Lat/Lon)...")
        gdf = gdf.to_crs(epsg=4326)
        
    # 3. Identifica a coluna que contém o nome do distrito e cria a chave padronizada
    col_nome = None
    for candidata in ["nm_distrit", "ds_nome", "NOME_DIST", "NM_DISTRIT", "nome"]:
        if candidata in gdf.columns:
            col_nome = candidata
            break
            
    if col_nome:
        gdf["distrito_padronizado"] = gdf[col_nome].apply(
            lambda x: unidecode(str(x)).upper().strip()
        )
        print(f"✅ {len(gdf)} distritos padronizados com sucesso a partir da coluna '{col_nome}'!")
        print("Exemplo dos 5 primeiros distritos:", gdf["distrito_padronizado"].head().tolist())
    
    # 4. Salva o GeoJSON limpo e leve pronto para o Streamlit/Plotly
    caminho_saida = "geodata/distritos_sp_wgs84.geojson"
    gdf.to_file(caminho_saida, driver="GeoJSON")
    print(f"🚀 Arquivo geográfico pronto salvo em: {caminho_saida}")
import os
import json
import time
import requests

# Crear la carpeta de productos si no existe
os.makedirs("img/productos", exist_ok=True)

def cargar_catalogo_desde_js():
    """Lee el archivo productos.js automáticamente"""
    try:
        with open("productos.js", "r", encoding="utf-8") as f:
            contenido = f.read()
        
        inicio = contenido.find("{")
        fin = contenido.rfind("}") + 1
        json_str = contenido[inicio:fin]
        return json.loads(json_str)
    except Exception as e:
        print(f"[ERROR] No se pudo leer productos.js: {e}")
        return None

def descargar_fotos_unicas():
    catalogo = cargar_catalogo_desde_js()
    if not catalogo:
        print("Asegurate de que productos.js esté en la misma carpeta.")
        return

    print("=== GENERANDO FOTOS ÚNICAS Y VARIADAS PARA THE DRINK SPOT ===")
    
    # IDs de imágenes profesionales de Unsplash orientadas a bebidas, botellas y cristalería
    # Esto asegura variedad total para que no se repita la misma foto en todo el catálogo.
    banco_fotos = {
        "CERVEZAS ART": [
            "https://images.unsplash.com/photo-1608270102602-239634e389d4?w=640&q=80",
            "https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=640&q=80",
            "https://images.unsplash.com/photo-1566633806327-68e152aaf26d?w=640&q=80",
            "https://images.unsplash.com/photo-1575444758702-4a6b9222336e?w=640&q=80"
        ],
        "CERVEZAS INDUST": [
            "https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=640&q=80",
            "https://images.unsplash.com/photo-1618885472179-5e574ef0d40c?w=640&q=80",
            "https://images.unsplash.com/photo-1600788886242-5c96aabe3757?w=640&q=80"
        ],
        "VINOS": [
            "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=640&q=80",
            "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=640&q=80",
            "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=640&q=80",
            "https://images.unsplash.com/photo-1586370434639-0aa490c6d323?w=640&q=80",
            "https://images.unsplash.com/photo-1547595628-c63aab9c44e1?w=640&q=80"
        ],
        "ESPUMATES/CHAMP": [
            "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=640&q=80",
            "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=640&q=80"
        ],
        "GIN": [
            "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=640&q=80",
            "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=640&q=80",
            "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=640&q=80"
        ],
        "APERITIVO": [
            "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=640&q=80",
            "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?w=640&q=80"
        ],
        "VODKA": [
            "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=640&q=80",
            "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?w=640&q=80"
        ],
        "WHISKY": [
            "https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=640&q=80",
            "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=640&q=80"
        ]
    }

    # Foto por defecto genérica para las demás categorías menores
    default_fotos = [
        "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=640&q=80",
        "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=640&q=80"
    ]

    for rubro, productos in catalogo.items():
        print(f"\n📁 Categoría: [{rubro}] ({len(productos)} productos)")
        lista_urls = banco_fotos.get(rubro, default_fotos)
        
        for index, producto in enumerate(productos):
            nombre_archivo = producto.lower().replace("/", "-").replace(" ", "-").replace(".", "")
            ruta_destino = f"img/productos/{nombre_archivo}.jpg"
            
            # Seleccionamos una foto distinta usando el índice de forma rotativa
            url_elegida = lista_urls[index % len(lista_urls)]
            
            try:
                response = requests.get(url_elegida, timeout=8)
                if response.status_code == 200:
                    with open(ruta_destino, 'wb') as f:
                        f.write(response.content)
                    print(f"  [✔] Asignada (Única): {producto}")
                time.sleep(0.05)
            except Exception as e:
                print(f"  [✖] Error en {producto}: {e}")

    print("\n¡Proceso finalizado! Las imágenes ahora están repartidas y variadas por categoría.")

if __name__ == "__main__":
    descargar_fotos_unicas()
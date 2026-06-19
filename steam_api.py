import requests

BASE_STEAM = "https://store.steampowered.com/api"
BASE_STEAMSPY = "https://steamspy.com/api.php"

def buscar_juegos(nombre: str) -> list[dict]:
    """Busca juegos por nombre usando la API oficial de Steam."""
    try:
        resp = requests.get(
            "https://store.steampowered.com/api/storesearch",
            params={"term": nombre, "l": "spanish", "cc": "AR"},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        palabras_excluir = ["soundtrack", "ost", "demo", "artbook", "trailer", "dlc", "pack", "bundle"]
        filtrados = [
            j for j in items
            if not any(p in j.get("name", "").lower() for p in palabras_excluir)
        ]
        return filtrados
    except Exception as e:
        return []

def obtener_detalle(appid: int) -> dict:
    """Trae info completa de un juego por su appid."""
    try:
        resp = requests.get(f"{BASE_STEAM}/appdetails", params={"appids": appid, "l": "spanish"}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data[str(appid)]["data"] if data[str(appid)]["success"] else {}
    except Exception as e:
        return {}

def obtener_steamspy(appid: int) -> dict:
    """Trae datos extra de SteamSpy (jugadores, tags, owners)."""
    try:
        resp = requests.get(BASE_STEAMSPY, params={"request": "appdetails", "appid": appid}, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {}
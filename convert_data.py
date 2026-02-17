import json
import os
import shutil
import pathlib

# Paths
BASE_DIR = pathlib.Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data" / "generated" / "2025" / "groente_data_benelux_binnenland_2025_FINAL.json"
ICONS_SOURCE_DIR = BASE_DIR / "static" / "icons"
PWA_ICONS_DIR = BASE_DIR / "pwa" / "icons"
OUTPUT_FILE = BASE_DIR / "pwa" / "taken.json"

# Constants
MONTHS = ["Januari", "Februari", "Maart", "April", "Mei", "Juni", 
          "Juli", "Augustus", "September", "Oktober", "November", "December"]

# Icon mapping logic from generate_poster_portrait.py
ICON_NAAM_OVERRIDES_DEF = {
    "Bieten": "rodebiet.png",
    "Doperwten": "erwten.png",
    "Komkommer": "buitenkomkommer.png",
    "Peper/Paprika": "paprikapeper.png",
    "Postelein": "postelein.png",
    "Savooiekool": "savoiekool.png",
    "Slabonen": "sperziebonen.png",
    "Sjalot": "sjalot.png",
    "Sluitkool (Rode & Witte)": "rodekool.png",
    "Spruitkool": "spruitkool.png",
    "Venkel": "knolvenkel.png",
    # Add corrections for keys
    "Rode kool": "rodekool.png",
    "Witte kool": "wittekool.png",
    "Witlof": "witlof.png",
    "Zoete aardappel": "zoeteaardappel.png",
    "Zwarte rammenas": "zwarterammenas.png",
    "Meloen": "watermeloen.png" # Fallback
}

GROENTE_NAAM_MAPPING = {
    'andijvie': 'Andijvie', 'artisjok': 'Artisjok', 'asperges': 'Asperges',
    'aardappel': 'Aardappel', 'aardpeer': 'Aardpeer', 'aubergine': 'Aubergine',
    'augurk': 'Augurk', 'bieten': 'Bieten', 'bladmosterd': 'Bladmosterd',
    'bleekselderij': 'Bleekselderij', 'bloemkool': 'Bloemkool', 'boerenkool': 'Boerenkool',
    'bosui': 'Bosui', 'broccoli': 'Broccoli', 'chinese_kool': 'Chinese kool',
    'courgette': 'Courgette', 'doperwten': 'Doperwten', 'droogbonen': 'Droogbonen',
    'groenlof': 'Groenlof', 'haverwortel': 'Haverwortel', 'kapucijners': 'Kapucijners',
    'kardoen': 'Kardoen', 'knoflook': 'Knoflook', 'knolselderij': 'Knolselderij',
    'knolvenkel': 'Knolvenkel', 'komkommer': 'Komkommer', 'koolraap': 'Koolraap',
    'koolrabi': 'Koolrabi', 'mais': 'Mais', 'meiraap': 'Meiraap', 'mesclun': 'Mesclun',
    'mizuna': 'Mizuna', 'nieuw_zeelandse_spinazie': 'Nieuw-Zeelandse spinazie',
    'paksoi': 'Paksoi', 'palmkool': 'Palmkool', 'paprika': 'Paprika',
    'paprika_peper': 'Peper/Paprika', 'pastinaak': 'Pastinaak', 'pepers': 'Pepers',
    'peulen': 'Peulen', 'physalis': 'Physalis', 'pompoen': 'Pompoen',
    'postelein': 'Postelein', 'prei': 'Prei', 'pronkbonen': 'Pronkbonen',
    'raapsteel': 'Raapsteel', 'rabarber': 'Rabarber', 'radicchio_rosso': 'Radicchio Rosso',
    'radijs': 'Radijs', 'rammenas': 'Rammenas', 'rode_kool': 'Rode kool',
    'romanesco': 'Romanesco', 'rucola': 'Rucola', 'savooiekool': 'Savooiekool',
    'schorseneren': 'Schorseneren', 'sjalot': 'Sjalot', 'slabonen': 'Slabonen',
    'sla': 'Sla', 'sluitkool': 'Sluitkool (Rode & Witte)', 'snijbiet': 'Snijbiet',
    'snijbonen': 'Snijbonen', 'snijselderij': 'Snijselderij', 'sojabonen': 'Sojabonen (Edamame)',
    'sperziebonen': 'Sperziebonen', 'spinazie': 'Spinazie', 'spitskool': 'Spitskool',
    'spruitkool': 'Spruitkool', 'sugarsnaps': 'Sugarsnaps', 'tatsoi': 'Tatsoi',
    'tomaat': 'Tomaat', 'tuinbonen': 'Tuinbonen', 'tuinkers': 'Tuinkers',
    'tuinmelde': 'Tuinmelde', 'ui': 'Ui', 'veldsla': 'Veldsla', 'venkel': 'Venkel',
    'watermeloen': 'Watermeloen', 'winterpostelein': 'Winterpostelein',
    'witte_kool': 'Witte kool', 'witlof': 'Witlof', 'wortel': 'Wortel',
    'wortelpeterselie': 'Wortelpeterselie', 'yacon': 'Yacon', 'zuring': 'Zuring',
    'zoete_aardappel': 'Zoete aardappel', 'zwarte_rammenas': 'Zwarte rammenas', 'meloen': 'Meloen'
}

def determine_icon_filename(groente_key, groente_naam):
    if groente_naam in ICON_NAAM_OVERRIDES_DEF:
        return ICON_NAAM_OVERRIDES_DEF[groente_naam]
    if groente_key in ('postelein', 'winterpostelein'):
        return 'postelein.png'
    return f"{groente_key}.png"

def copy_icon(filename):
    if not os.path.exists(PWA_ICONS_DIR):
        os.makedirs(PWA_ICONS_DIR)
    
    # Search in multiple locations
    search_dirs = [
        ICONS_SOURCE_DIR,
        ICONS_SOURCE_DIR / "optimized",
        ICONS_SOURCE_DIR / "Colab",
        ICONS_SOURCE_DIR / "Def"
    ]
    
    src = None
    for d in search_dirs:
        possible_src = d / filename
        if possible_src.exists():
            src = possible_src
            break
            
    if src and src.exists():
        dst = PWA_ICONS_DIR / filename
        shutil.copy2(src, dst)
        return True
    return False

def format_week(week_num):
    # Determine month index (0-11) based on week number
    # Simple approx: week 1-4 jan, 5-8 feb etc.
    # Logic from poster: thursday of week determines month
    import datetime
    # Use 2025 as base year
    try:
        d = datetime.date.fromisocalendar(2025, week_num, 4) # Thursday
        return MONTHS[d.month - 1]
    except ValueError:
        return "?"

def main():
    print("Starting conversion...")
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if "data" in data:
            data = data["data"]
            
    tasks = []
    
    # Ensure icon dir exists
    if not os.path.exists(PWA_ICONS_DIR):
        os.makedirs(PWA_ICONS_DIR)

    for vegetable_key, entries in data.items():
        groente_naam = GROENTE_NAAM_MAPPING.get(vegetable_key, vegetable_key.title())
        icon_filename = determine_icon_filename(vegetable_key, groente_naam)
        
        # Copy the icon
        if not copy_icon(icon_filename):
            print(f"Warning: Icon not found for {vegetable_key}: {icon_filename}")
            # Try default fallback? default.png
            if copy_icon("Default.png"):
                icon_filename = "Default.png"
        
        if not isinstance(entries, list):
            continue

        for entry in entries:
            variant = entry.get('variant_poster', 'Standaard')
            fase = entry.get('fase_poster', 'Onbekend').title() # Title case for display
            tip = entry.get('tip', '')
            variant_desc = entry.get('variant', '') # Full description
            
            for batch in entry.get('batch_details', []):
                start_week = batch.get('start_week')
                end_week = batch.get('end_week')
                
                # Create a task for the START week (most important action moment)
                # But maybe we want tasks for every month in range?
                # The prompt asks for: "1000 items: Groente, Maand, Taak, Beschrijving"
                # A task implies an action. "Starten met" is the best action.
                
                month_name = format_week(start_week)
                month_nr = MONTHS.index(month_name) + 1 # 1-12
                
                task = {
                    "id": f"{vegetable_key}-{variant}-{fase}-{start_week}",
                    "groente": groente_naam,
                    "icoon": icon_filename,
                    "maand": month_name,
                    "maand_nr": month_nr,
                    "week": start_week,
                    "fase": fase,
                    "variant": variant,
                    "beschrijving": variant_desc,
                    "tip": tip,
                    "weken_display": f"Week {start_week}" if start_week == end_week else f"Week {start_week}-{end_week}"
                }
                tasks.append(task)
                
    # Sort tasks by start week
    tasks.sort(key=lambda x: (x['week'], x['groente']))
    
    print(f"Generated {len(tasks)} tasks.")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
        
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

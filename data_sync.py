## Script that automatically synchronizes data from unicorn notes on the atmo server. Has to be run locally with activated wireguard


#%%
import os
import paramiko
import datetime
from scp import SCPClient
from datetime import datetime, timezone
#%%

# Konfiguration
sensor_ips = {
    "unicorn01": "192.168.11.31",
    "unicorn02": "192.168.11.32",
    "unicorn03": "192.168.11.33",
    "unicorn04": "192.168.11.34",
    "unicorn05": "192.168.11.35",
    "unicorn06": "192.168.11.36",
    "unicorn07": "192.168.11.37",
    "unicorn08": "192.168.11.38",
    "unicorn09": "192.168.11.39",
    "unicorn10": "192.168.11.40",
    "unicorn11": "192.168.11.41",
    "unicorn12": "192.168.11.42",
    "unicorn13": "192.168.11.43",
    "unicorn14": "192.168.11.44",
    "unicorn15": "192.168.11.45",
    "unicorn16": "192.168.11.46",
    "unicorn17": "192.168.11.47",
    "unicorn18": "192.168.11.48",
}
sensor_user = "beacon"
sensor_pass = {"unicorn01": "CO2unicorn2401", 
               "unicorn02" : "CO2unicorn2402",
               "unicorn03" : "CO2unicorn2403",
                "unicorn04" : "CO2unicorn2404",
                "unicorn05" : "CO2unicorn2405",
                "unicorn06" : "CO2unicorn2406",
                "unicorn07" : "CO2unicorn2407",
                "unicorn08" : "CO2unicorn2408",
                "unicorn09" : "CO2unicorn2409",
                "unicorn10" : "CO2unicorn2410",
                "unicorn11" : "CO2unicorn2411",
                "unicorn12" : "CO2unicorn2412",
                "unicorn13" : "CO2unicorn2413",
                "unicorn14" : "CO2unicorn2414",
                "unicorn15" : "CO2unicorn2415",
                "unicorn16" : "CO2unicorn2416",
                "unicorn17" : "CO2unicorn2417",
                "unicorn18" : "CO2unicorn2418",
               
}    
server_ip = "dsvr-02.iup.uni-heidelberg.de"
server_user = "hermes"
server_pass = "PerAsperaAdAstra"
server_target_dir = "/mnt/data2/UNICORN/raw_data"

local_temp_dir = "C:/Users/atmo-user/Documents/MA/temp_download"

#%%

# Hilfsfunktionen
def create_ssh_client(ip, user, password, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=password, port=port)
    return client

# Alle .csv-Dateien im Verzeichnis listen
def list_remote_files(ssh, path):
    stdin, stdout, stderr = ssh.exec_command(f'find {path} -type f -name "*.csv"')
    return [line.strip() for line in stdout.readlines()]

# Aktuelle Datei (laufende Stunde) ermitteln
def current_hour_file():
    now = datetime.now(timezone.utc)
    return f"{now:%Y_%m_%d-%H}.csv"

# Datum aus Dateiname extrahieren
def extract_datetime_from_filename(filename):
    try:
        parts = filename.split("-")[-1].replace(".csv", "")
        return datetime.strptime(parts, "%Y_%m_%d-%H")
    except Exception:
        return datetime.min

def main():
    print("[*] Verbinde zum Server...")
    try:
        server_ssh = create_ssh_client(server_ip, server_user, server_pass, port=49200)
    except Exception as e:
        print(f"[X] Verbindung zum Server fehlgeschlagen: {e}")
        return

    server_files = list_remote_files(server_ssh, server_target_dir)
    server_filenames = set(os.path.basename(f) for f in server_files)
    print(f"[•] Dateien auf Server: {len(server_filenames)} bekannt")


    for name, ip in sensor_ips.items():
        print(f"\n[*] Bearbeite Sensor {name} ({ip})")
        
        curr_file = 'DEnode'+str(int(name[-2:]))+'-'+current_hour_file()
        print(f"[•] Aktuelle Datei wird ausgeschlossen: {curr_file}")

        try:
            sensor_ssh = create_ssh_client(ip, sensor_user, sensor_pass[name])
        except Exception as e:
            print(f"[!] Verbindung zu {name} fehlgeschlagen: {e}")
            continue

        # Monatsordner abrufen
        month_dirs = []
        try:
            stdin, stdout, stderr = sensor_ssh.exec_command("ls -1 /home/beacon/data/")
            month_dirs = [line.strip() for line in stdout if line.strip().startswith("20")]
            month_dirs = [
                d for d in month_dirs
                if d >= "2025_09" and len(d) == 7
            ]
        except Exception as e:
            print(f"[!] Fehler beim Abrufen der Monatsverzeichnisse von {name}: {e}")
            continue

        if not month_dirs:
            print(f"[!] Keine gültigen Monatsverzeichnisse bei {name} gefunden.")
            continue

        for month in sorted(month_dirs):
            remote_month_path = f"/home/beacon/data/{month}"
            print(f"\n[📁] Monat {month} auf {name}...")

            try:
                stdin, stdout, stderr = sensor_ssh.exec_command(f"ls -1 {remote_month_path}/*.csv")
                sensor_files = [line.strip() for line in stdout if line.strip().endswith(".csv")]
            except Exception as e:
                print(f"[!] Fehler beim Abrufen von Dateien in {remote_month_path}: {e}")
                continue

            if not sensor_files:
                print(f"[!] Keine Dateien gefunden in {remote_month_path}")
                continue

            files_to_sync = [
            f for f in sensor_files
            if os.path.basename(f) != curr_file and os.path.basename(f) not in server_filenames
            ]

            total = len(files_to_sync)

            for idx, filepath in enumerate(files_to_sync, 1):
                filename = os.path.basename(filepath)
                print(f"[{idx}/{total}] Lade {filename} von {name} herunter...")
            
                
                if filename == curr_file:
                    print(f"[→] Datei {filename} wird übersprungen (noch nicht fertig)")
                    continue

                if filename in server_filenames:
                    print(f"[✓] Datei {filename} bereits vorhanden → übersprungen")
                    continue

                try:
                    with SCPClient(sensor_ssh.get_transport()) as scp:
                        local_tmp = f"./tmp_{filename}"
                        scp.get(filepath, local_path=local_tmp)

                    with SCPClient(server_ssh.get_transport()) as scp:
                        target_path = f"{server_target_dir}/{name}/{filename}"
                        scp.put(local_tmp, target_path)

                    os.remove(local_tmp)

                except Exception as e:
                    print(f"[!] Fehler beim Übertragen von {filename}: {e}")
                    continue

    print("\n[✔] Synchronisation abgeschlossen.")

if __name__ == "__main__":
    main()
# %%

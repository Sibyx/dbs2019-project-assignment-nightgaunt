# MdnsWeb

Digitálna databáza exemplárov v entomoligickej zbierke. Systém je implementovaný ako webová aplikácia, prístupná on-line.
Systém slúži na vytváranie, kategorizovanie a vyhľadávanie záznamov. Zároveň umožnuje generovanie QR štítkov,
správu zapožcaných exemplárov a základný štatistický prehľad o zbierke formou jednoduche dahsboard. Správa aplikácie
je umožnená iba autorizovaným používateľom, možnosť prezerania a vyhľadávania je pre všetkých návštevníkov.
Súčasťou je jednoduchý import/export mechanizmus.

Back-end je implementovaný ako [Django](https://www.djangoproject.com/) aplikácia pre Python 3.6 a na front-end 
je pre zjednodušenie použitá knižnica [Bootstrap](https://getbootstrap.com/). Ako databázový systém je použitý 
[PostgreSQL](https://www.postgresql.org/) server verzie 10.

Všeky issues (feature, bug, docs a enchasment) sú spravované cez príslušné GitHub nástroje:

- [GitHub Issues](https://github.com/fiit-dbs-2019/dbs2019-project-assignment-nightgaunt/issues).
- [GitHub Projects](https://github.com/fiit-dbs-2019/dbs2019-project-assignment-nightgaunt/projects).

Celá špecifikácia a dokumentácia k projektu sa nachádza v 
[GitHub Wiki](https://github.com/fiit-dbs-2019/dbs2019-project-assignment-nightgaunt/wiki).

V projekte používame codestyle poďla [PEP8](https://www.python.org/dev/peps/pep-0008/) a na správu codebase
aplikujeme techniku [git-flow](https://datasift.github.io/gitflow/IntroducingGitFlow.html):

- `master` vetva obsahuje vždy stabilnú verziu zdrojového kódu
- `develop` vetva obsahuje zmeny implementované v rámci daného behu/milestonu
- `feature/*` vetvy obsahuju implementácie konkrétnych issues/features

Po dokončení konkrétnej issue vytváram Pull Request do `develop` vetvy a pri každom uzavretom milestone
robím merge to `master` vetvy.

## Inštalácia

Minimálne požiadavky:

- Python 3.6
- Pipenv
- PostgreSQL
- NodeJS & yarn (pre úspešný build front-end časti)

Na správu závislostí používame [pipenv](https://github.com/pypa/pipenv), ktorý inštaláciu značne zjednodušuje:

Nižšie napísaný príklad inštalácie pomocou Git-u stiahne codebase projektu a spustí nad ním príklad `pipenv install`,
ktorý vytvorí virtualenv prostredie, do ktorého nainštaluje všetky projektové dependencies. 

```bash
git clone git@github.com:fiit-dbs-2019/dbs2019-project-assignment-nightgaunt.git MdnsWeb
cd MdnsWeb
pipenv install
```

## Knižnice

- [Django](https://www.djangoproject.com/): Back-end framework
- [Bootstrap](https://getbootstrap.com/): Front-end framework
- [python-dotenv](https://github.com/theskumar/python-dotenv): Konfigurácia
- [django-role-permissions](https://github.com/vintasoftware/django-role-permissions): RBAC
- [python-qrcode](https://github.com/lincolnloop/python-qrcode): QR code generator
- [bootstrap-table](https://bootstrap-table.com/): Bootstrap native datatables

---
S ❤️ Jakub Dubec (c) 2019

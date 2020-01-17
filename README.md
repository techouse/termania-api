# Termania.net API - Python Client

A Python wrapper for the Termania.net REST API. Easily interact with the Termania.net REST API using this library.

## Installation

```bash
pip install termania
```

## Getting started

Prior to using this library you will have to request a **licence key** from [Termania.net](mailto:info@amebis.si?subject=Request%20for%20Termania.net%20license%20key).

## Setup

```python
from termania import API

termania_api = API(licence_key=1234567890)
```

### Options

|    Option     | Type  | Required |      Description     |
|:-------------:|:-----:|:--------:|:--------------------:|
| `license_key` | `int` |   yes    | Your API license key |


### Methods

#### Search
```python
entry = termania_api.search(query="mama", dictionary_id=70)
```

|   Parameter   |  Type | Required |                    Description                   |
|:-------------:|:-----:|:--------:|:------------------------------------------------:|
|     query     | `str` |    yes   |                 Your search query                |
| dictionary_id | `int` |    yes   | The dictionary you want to search your query for |

##### Returns
```python
Entry(
    dictionary_id=70, 
    entry_id=743367, 
    headword="mama", 
    html="""<p xmlns="http://www.w3.org/1999/xhtml" xmlns:e="urn:STP_XMLDATA">
             <span class="color_orange font_xlarge strong">mama </span>
             <span class="color_lightdark font_small italic">(slovensko) </span>
             <span class="color_lightdark font_small">samostalnik, </span>
             <span class="color_lightdark font_small">ž. sp. </span>
             <br/>
             <br/>
             <span class="italic font_small color_lightdark">Oblike: </span>
             <span class="">mam, mamah, mamam, mamama, mamami, mame, mami, mamo </span>
                 <hr style="color: #e3e3e3;background-color: #e3e3e3; height: 1px;border: 0 none;"/>
                 <span class="">
                         <span class="italic font_small color_lightdark">Pomen: </span>
                         <span class="color_orange">sorodnik </span>
                         <br/>
                         <span class="italic font_small color_lightdark">Povezava spredaj: </span>
                         <span class="font_large">rôden, pokojen </span>
                         <span class="color_lightdark font_small italic"><br/>Slovenska sopomenka: </span>
                         <span class="font_large">mati</span>, 
                         <span class="font_large">roditeljica</span>, 
                         <span class="font_large">rodnica</span>
                         <span class="color_lightdark font_small italic"><br/>Angleški prevod: </span>
                         <span class="color_dark font_xlarge">mother</span>
                         <span class="color_lightdark font_small italic"><br/>Nemški prevod: </span>
                         <span class="color_dark font_xlarge">Mutter</span>, 
                         <span class="color_dark font_xlarge">Mama</span>, 
                         <span class="color_dark font_xlarge">Mom</span>
                         <span class="color_lightdark font_small italic"><br/>Albanski prevod: </span>
                         <span class="color_dark font_xlarge">nënë</span>, 
                         <span class="color_dark font_xlarge">mëmë</span>
                         <span class="color_lightdark font_small italic"><br/>Francoski prevod: </span>
                         <span class="color_dark font_xlarge">mère</span>
                 </span>
                 <hr style="color: #e3e3e3;background-color: #e3e3e3; height: 1px;border: 0 none;"/>
                 <!-- etc ... trimmed to keep the README manageable -->
         </p>""")
```

#### Get dictionary list
```python
dictionaries = termania_api.get_dictionaries()
```

##### Returns
```python
{
    6: Dictionary(id=6, name='Grško-slovenski slovar', author='Anton Dokler', languages=('el', 'sl'), lingualism=2, type=1), 
    8: Dictionary(id=8, name='Besedišče slovenskega jezika z oblikoslovnimi podatki', author='ZRC SAZU, Inštitut za slovenski jezik Frana Ramovša in avtorji', languages=('sl', 'sl'), lingualism=1, type=1), 
    # etc ... trimmed to keep the README manageable
}
```

## Testing

```bash
git clone https://github.com/techouse/termania-api
cd termania-api                  
python3 -m venv env
source env/bin/activate
pip install -e .
pip install -r requirements_dev.txt
tox
```
from dbnomics_fetcher_toolbox.sdmx_utils.normalization import normalize_sdmx_file_header
from dbnomics_fetcher_toolbox.sdmx_utils.v2_1.structure_parsers import StructureSpecificDataParser
from tests.conftest import MakeTmpFile


def test_multiple_lines(make_tmp_file: MakeTmpFile) -> None:
    sdmx_text = """<?xml version='1.0' encoding='UTF-8'?>
<message:StructureSpecificData xmlns:ss="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific" xmlns:footer="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message/footer" xmlns:ns1="urn:sdmx:org.sdmx.infomodel.datastructure.Dataflow=FR1:INDICE-TRAITEMENT-FP(1.0):ObsLevelDim:TIME_PERIOD" xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xml="http://www.w3.org/XML/1998/namespace">
  <message:Header>
    <message:ID>INDICE-TRAITEMENT-FP_1728381812291</message:ID>
    <message:Test>false</message:Test>
    <message:Prepared>2024-09-27T17:12:02.793+02:00</message:Prepared>
    <message:Sender id="FR1">
      <common:Name xml:lang="fr">Institut national de la statistique et des études économiques</common:Name>
    </message:Sender>
    <message:Structure structureID="FR1_INDICE-TRAITEMENT-FP_1_0" namespace="urn:sdmx:org.sdmx.infomodel.datastructure.Dataflow=FR1:INDICE-TRAITEMENT-FP(1.0):ObsLevelDim:TIME_PERIOD" dimensionAtObservation="TIME_PERIOD">
      <common:StructureUsage>
        <Ref agencyID="FR1" id="INDICE-TRAITEMENT-FP" version="1.0"/>
      </common:StructureUsage>
    </message:Structure>
    <message:Source xml:lang="fr">Banque de données macro-économiques</message:Source>
  </message:Header>
  <message:DataSet ss:dataScope="DataStructure" xsi:type="ns1:DataSetType" ss:structureRef="FR1_INDICE-TRAITEMENT-FP_1_0">
    <Series UNIT_MEASURE="SO" CATEGORIE_FP="T" NATURE="VALEUR_ABSOLUE" REF_AREA="FM" BASIND="2000-T4" CORRECTION="BRUT" FREQ="T" UNIT_MULT="0" INDICATEUR="NSALBF" IDBANK="001572130" TITLE_FR="Indice de traitement brut - Grille indiciaire pour l'ensemble des catégories - Base 100 en 2000" TITLE_EN="Gross wage index - Wage scale for all categories of civil servants - Base 100 in 2000" LAST_UPDATE="2024-09-19" DECIMALS="2">
      <Obs TIME_PERIOD="2024-Q2" OBS_VALUE="126.15" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/><Obs TIME_PERIOD="2024-Q1" OBS_VALUE="126.11" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2023-Q4" OBS_VALUE="124.9" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2023-Q3" OBS_VALUE="124.79" OBS_STATUS="A" OBS_REV="1" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2023-Q2" OBS_VALUE="124.82" OBS_STATUS="A" OBS_REV="1" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2023-Q1" OBS_VALUE="122.81" OBS_STATUS="A" OBS_REV="1" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2022-Q4" OBS_VALUE="122.73" OBS_STATUS="A" OBS_REV="1" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2022-Q3" OBS_VALUE="122.71" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2022-Q2" OBS_VALUE="118.51" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2022-Q1" OBS_VALUE="118.42" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
    </Series>
  </message:DataSet>
</message:StructureSpecificData>
"""
    with make_tmp_file(sdmx_text) as sdmx_file:
        normalize_sdmx_file_header(
            sdmx_file,
            xpaths=[
                "/message:StructureSpecificData/message:Header/message:ID",
                "/message:StructureSpecificData/message:Header/message:Prepared",
            ],
        )
        parser = StructureSpecificDataParser.from_xml_file(sdmx_file)
        assert parser.get_text("./message:Header/message:ID") == "REDACTED"
        assert parser.get_text("./message:Header/message:Prepared") == "REDACTED"


def test_oneline_multiple_elements(make_tmp_file: MakeTmpFile) -> None:
    sdmx_text = """<?xml version='1.0' encoding='UTF-8'?>
<message:StructureSpecificData xmlns:ss="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific" xmlns:footer="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message/footer" xmlns:ns1="urn:sdmx:org.sdmx.infomodel.datastructure.Dataflow=FR1:INDICE-TRAITEMENT-FP(1.0):ObsLevelDim:TIME_PERIOD" xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xml="http://www.w3.org/XML/1998/namespace">
  <message:Header>
    <message:ID>INDICE-TRAITEMENT-FP_1728381812291</message:ID><message:Test>false</message:Test><message:Prepared>2024-09-27T17:12:02.793+02:00</message:Prepared>
    <message:Sender id="FR1">
      <common:Name xml:lang="fr">Institut national de la statistique et des études économiques</common:Name>
    </message:Sender>
    <message:Structure structureID="FR1_INDICE-TRAITEMENT-FP_1_0" namespace="urn:sdmx:org.sdmx.infomodel.datastructure.Dataflow=FR1:INDICE-TRAITEMENT-FP(1.0):ObsLevelDim:TIME_PERIOD" dimensionAtObservation="TIME_PERIOD">
      <common:StructureUsage>
        <Ref agencyID="FR1" id="INDICE-TRAITEMENT-FP" version="1.0"/>
      </common:StructureUsage>
    </message:Structure>
    <message:Source xml:lang="fr">Banque de données macro-économiques</message:Source>
  </message:Header>
  <message:DataSet ss:dataScope="DataStructure" xsi:type="ns1:DataSetType" ss:structureRef="FR1_INDICE-TRAITEMENT-FP_1_0">
    <Series UNIT_MEASURE="SO" CATEGORIE_FP="T" NATURE="VALEUR_ABSOLUE" REF_AREA="FM" BASIND="2000-T4" CORRECTION="BRUT" FREQ="T" UNIT_MULT="0" INDICATEUR="NSALBF" IDBANK="001572130" TITLE_FR="Indice de traitement brut - Grille indiciaire pour l'ensemble des catégories - Base 100 en 2000" TITLE_EN="Gross wage index - Wage scale for all categories of civil servants - Base 100 in 2000" LAST_UPDATE="2024-09-19" DECIMALS="2">
      <Obs TIME_PERIOD="2024-Q2" OBS_VALUE="126.15" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/><Obs TIME_PERIOD="2024-Q1" OBS_VALUE="126.11" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2023-Q4" OBS_VALUE="124.9" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2023-Q3" OBS_VALUE="124.79" OBS_STATUS="A" OBS_REV="1" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2023-Q2" OBS_VALUE="124.82" OBS_STATUS="A" OBS_REV="1" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2023-Q1" OBS_VALUE="122.81" OBS_STATUS="A" OBS_REV="1" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2022-Q4" OBS_VALUE="122.73" OBS_STATUS="A" OBS_REV="1" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2022-Q3" OBS_VALUE="122.71" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2022-Q2" OBS_VALUE="118.51" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
      <Obs TIME_PERIOD="2022-Q1" OBS_VALUE="118.42" OBS_STATUS="A" OBS_QUAL="DEF" OBS_TYPE="A"/>
    </Series>
  </message:DataSet>
</message:StructureSpecificData>
"""
    with make_tmp_file(sdmx_text) as sdmx_file:
        normalize_sdmx_file_header(
            sdmx_file,
            xpaths=[
                "/message:StructureSpecificData/message:Header/message:ID",
                "/message:StructureSpecificData/message:Header/message:Prepared",
            ],
        )
        parser = StructureSpecificDataParser.from_xml_file(sdmx_file)
        assert parser.get_text("./message:Header/message:ID") == "REDACTED"
        assert parser.get_text("./message:Header/message:Prepared") == "REDACTED"

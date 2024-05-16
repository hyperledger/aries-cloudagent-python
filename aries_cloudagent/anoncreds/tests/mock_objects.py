MOCK_PRES_REQ = {
    "nonce": "182453895158932070575246",
    "name": "Step 3 Send your Health Information",
    "version": "1.0",
    "requested_attributes": {
        "biomarker_attrs_0": {
            "names": [
                "name",
                "concentration",
                "unit",
                "range",
                "collected_on",
                "biomarker_id",
                "researcher_share",
            ],
            "restrictions": [
                {"schema_name": "MYCO Biomarker", "attr::name::value": "Iron"}
            ],
        },
        "consent_attrs": {
            "restrictions": [
                {
                    "schema_name": "MYCO Consent Enablement",
                    "schema_version": "0.1.0",
                    "attr::jti_unique_identifier::value": "205b1ea0-7848-48d4-b52b-339122d84f62",
                }
            ],
            "name": "jti_unique_identifier",
        },
    },
    "requested_predicates": {},
}

MOCK_PRES = {
    "proof": {
        "proofs": [
            {
                "primary_proof": {
                    "eq_proof": {
                        "revealed_attrs": {
                            "biomarker_id": "33034450023603237719386825060766757598085121996569112944281451290292212516012",
                            "collected_on": "92231735610070911075924224447204218356256133056723930517696107260511721601349",
                            "concentration": "10",
                            "name": "85547618788485118809771015708850341281587970912661276233439574555663751388073",
                            "range": "106828626115908025842177441696860557581575579893927923198365300598359723920768",
                            "researcher_share": "101264834079306301897660576123112461042861436742738894013248454492965796383403",
                            "unit": "38351211041892038382023569421847544683371072212679556578649761181279472893849",
                        },
                        "a_prime": "80156520245352052628208149565161465200964633377479145197038408116901327106468493831807000641577246417448908134495822028339761705905365398613527463662816881507291787145610182891716009505407072490691097943029471835157968113065071523597746984296197661560454442163361095634052138951650373193896962906203169809352467024247772052836999799731422581068645748537557874869718897034120634529002420631012358510111427944993245065350416694516913472010105229188198167306183788520891926236449848811955646933539477960935319919207451858981065765523367984374104834278565184338252025155136368869580505679884921590811310587077071610172673",
                        "e": "115602723672843258810892161808995599340414281260248127600708536325470178701996999306086286379312077726886107268519700961209712187789855371",
                        "v": "1250383260306407741656763352595256748825474237767244783206569756476708112785930898966696687140808011529311298553822794830872826226191807175199015541611342880032928005827271961840046208463350458298210749103878893742434685172894883857423865293195542824393317226300133796527531436931435189766065404966370796699897584860421160155369018136946091524266742514828667575397735892093187106092545876795688095293610064164136737808333322708435913545499149948994191514980395955519036106660001526586674248282052492138917987323789012051794441548696998993861159018178474063785171288325900474499496141522583368982451169653258746506425495702762445790848698570457196767532483566475068200091609719957656394696938689265240025099424248587121592521826940348286940172887963179718337593603053496022182071613592070622825622277436966372346642772481567879001423472517233061740522533372490151585309457871632521280719357505751796940152868034526426510835",
                        "m": {
                            "master_secret": "3455871040557234123393960708120725061759594951341120214330342075748561632734634451036095543889895409812764789858455375956895105746442946098665140470124325622343440794421325163223",
                            "client_share": "4233663763294709836704307308997831519311512039775169744174375585917035614714239153287862168426091336550799195245481707264207548331415960277065672755643752404180562900805493953484",
                        },
                        "m2": "12942698897200869280316481431207639453433287089474860040781378232999349549981799159560238504559317917040820580596635945161264308025301203452846862479261473387068350544024561412435",
                    },
                    "ge_proofs": [],
                }
            },
            {
                "primary_proof": {
                    "eq_proof": {
                        "revealed_attrs": {
                            "jti_unique_identifier": "46414468020333259158238797309781111434265856695713363124410805958145233348633"
                        },
                        "a_prime": "52825780315318905340996188008133401356826233601375100674436798295026172087388431332751168238882607201020021795967828258295811342078457860422414605408183505911891895360825745994390769724939582542658347473498091021796952186290990181881158576706521445646669342676592451422000320708168877298354804819261007033664223006892049856834172427934815827786052257552492013807885418893279908149441273603109213847535482251568996326545234910687135167595657148526602160452192374611721411569543183642580629352619161783646990187905911781524203367796090408992624211661598980626941053749241077719601278347846928693650092940416717449494816",
                        "e": "40342480172543061520030194979861449480343743039487113094246205723322643070249538229638327935935486373873622430409109409257546971244601965",
                        "v": "217871997575635857881367472262154388060800564043554848081521162883333745687724235201324121915821236796357195214089699645741515836727882126142579489701412861659136426497703162695983681701205672924385915403141611021784136285588350763399255203187442277784718461565122805239422370067600654500115262174706580098147603414365915243447789285877195068031630371954678432401446457453517813298670236942253026249413255471803997869331683293818651006043399070308083119054618677128448043841313844695654424369871669436628257531643623230026240200330490039607166147891705813033761093730859310423856156850596341547950105490585959768382544221555877471751940512766452511773683786023245283041103270102119125303027835868565240336923422734962345750992898991606841120358203160628015844345063465293475128118937815965000466081345494616126511595974927544434058100817176268040385848789013718618727873445834393897904247054897801708217939187593785671914",
                        "m": {
                            "iat_consent_timestamp": "7919242808448912829024078929834347184203169048480606699350973804205285806978474375691141504249426249676222104091995582731720654507393708298132400435805626192291975477967402460279",
                            "master_secret": "3455871040557234123393960708120725061759594951341120214330342075748561632734634451036095543889895409812764789858455375956895105746442946098665140470124325622343440794421325163223",
                            "data_controller": "16070549690575784944224634793654539357398383214512772967411296056738507137421264813779497172425030465490587794790393434847583852932544021088761347641812155158324233253206392974293",
                            "notice": "2790610958721083178459621377821800672322230987466716467063649577108407884592339521820875278264969393963213925568888672412150769438560815981777952572004955362915245795447078373509",
                            "sensitive": "13552814315985495030467505807226704038231487014593307078913973520081443107274508887651839292151852713782653522711975492131914644109941607616672243509214979259100892541150351227883",
                            "services": "14860984314279608355643170908802532226194914773406547259519961082467311361623076451869406343140860447342041426195737612897540117192702117380288330928866665314831926780606136352645",
                            "sub_subject_identifier": "11736177517163751882849070942823049196298287414132249166618760803125435466270948777194044507635346721244111946358927525083691171695431736819244809221351813271261283779276670885101",
                            "moc_method_of_collection": "10026360820367693771310999595495505533281326977349798360729122862705999157070660881611421445424239119786180921960380892002204780026072600494332540208429642332890963846523547470729",
                            "jurisdiction_data_processing": "15829143141425514118932461858094583045441924952665872659029333578019676797278419825311275014912077620757631693167948665554731430154156737419706553672424812320891308795411687679270",
                            "iss_internet_processing_uri": "6900796243066434651671715348976599009606292569990892886896520779618011026060325075822786686418461731663661832508437549373109822105600719490952253743950241384782222356411498407620",
                            "version_consent_specification": "7796257942256624260327966366702213561879098947042014532961291550019706546662478888172243088973621029223408695289700984802154645011280488167967047321149956253054269901250137513345",
                            "policy_url": "12241676508867847022708464707584814145889660003604359058532137895063826021524887759921830911553663255421852525705197991376264187781979066233701110706958983099645275940668404311601",
                        },
                        "m2": "6509130065158989037891281073557909501783443634141673890142284302459280804904096303151728187237486991775852971807701594247754409108836089746736345158069365449802597798950172729241",
                    },
                    "ge_proofs": [],
                }
            },
        ],
        "aggregated_proof": {
            "c_hash": "81763443376178433216866153835042672285397553441148068557996780431098922863180",
            "c_list": [
                [2, 122, 246, 66, 85, 35, 17, 213, 1],
                [1, 162, 117, 246, 95, 154, 129, 32],
            ],
        },
    },
    "requested_proof": {
        "revealed_attrs": {
            "consent_attrs": {
                "sub_proof_index": 1,
                "raw": "205b1ea0-7848-48d4-b52b-339122d84f62",
                "encoded": "46414468020333259158238797309781111434265856695713363124410805958145233348633",
            }
        },
        "revealed_attr_groups": {
            "biomarker_attrs_0": {
                "sub_proof_index": 0,
                "values": {
                    "researcher_share": {
                        "raw": "bf712cb328a92862b57f0dc806dec12a",
                        "encoded": "101264834079306301897660576123112461042861436742738894013248454492965796383403",
                    },
                    "unit": {
                        "raw": "μM",
                        "encoded": "38351211041892038382023569421847544683371072212679556578649761181279472893849",
                    },
                    "concentration": {"raw": "10", "encoded": "10"},
                    "name": {
                        "raw": "Iron",
                        "encoded": "85547618788485118809771015708850341281587970912661276233439574555663751388073",
                    },
                    "range": {
                        "raw": "9.00-30.0",
                        "encoded": "106828626115908025842177441696860557581575579893927923198365300598359723920768",
                    },
                    "collected_on": {
                        "raw": "2020-07-05",
                        "encoded": "92231735610070911075924224447204218356256133056723930517696107260511721601349",
                    },
                    "biomarker_id": {
                        "raw": "c9ace7dc-0485-4f3f-b466-16a27a80acf1",
                        "encoded": "33034450023603237719386825060766757598085121996569112944281451290292212516012",
                    },
                },
            }
        },
        "self_attested_attrs": {},
        "unrevealed_attrs": {},
        "predicates": {},
    },
    "identifiers": [
        {
            "schema_id": "CsQY9MGeD3CQP4EyuVFo5m:2:MYCO Biomarker:0.0.3",
            "cred_def_id": "CsQY9MGeD3CQP4EyuVFo5m:3:CL:14951:MYCO_Biomarker",
        },
        {
            "schema_id": "FbozHyf7j5q7TDn2s8MXZN:2:MYCO Consent Enablement:0.1.0",
            "cred_def_id": "TUku9MDGa7QALbAJX4oAww:3:CL:531757:MYCO_Consent_Enablement",
        },
    ],
}

MOCK_SCHEMA = {
    "issuerId": "https://example.org/issuers/74acabe2-0edc-415e-ad3d-c259bac04c15",
    "name": "Example schema",
    "version": "0.0.1",
    "attrNames": ["name", "age", "vmax"],
}

MOCK_CRED_DEF = {
    "issuerId": "did:indy:sovrin:SGrjRL82Y9ZZbzhUDXokvQ",
    "schemaId": "did:indy:sovrin:SGrjRL82Y9ZZbzhUDXokvQ/anoncreds/v0/SCHEMA/MemberPass/1.0",
    "type": "CL",
    "tag": "latest",
    "value": {
        "primary": {
            "n": "779...397",
            "r": {
                "birthdate": "294...298",
                "birthlocation": "533...284",
                "citizenship": "894...102",
                "expiry_date": "650...011",
                "facephoto": "870...274",
                "firstname": "656...226",
                "link_secret": "521...922",
                "name": "410...200",
                "uuid": "226...757",
            },
            "rctxt": "774...977",
            "s": "750..893",
            "z": "632...005",
        },
        "revocation": {
            "g": "1 154...813 1 11C...D0D 2 095..8A8",
            "g_dash": "1 1F0...000",
            "h": "1 131...8A8",
            "h0": "1 1AF...8A8",
            "h1": "1 242...8A8",
            "h2": "1 072...8A8",
            "h_cap": "1 196...000",
            "htilde": "1 1D5...8A8",
            "pk": "1 0E7...8A8",
            "u": "1 18E...000",
            "y": "1 068...000",
        },
    },
}


MOCK_SCHEMAS = {
    "CsQY9MGeD3CQP4EyuVFo5m:2:MYCO Biomarker:0.0.3": {"value": {}},
    "FbozHyf7j5q7TDn2s8MXZN:2:MYCO Consent Enablement:0.1.0": {"value": {}},
}

MOCK_CRED_DEFS = {
    "CsQY9MGeD3CQP4EyuVFo5m:3:CL:14951:MYCO_Biomarker": {"value": {}},
    "TUku9MDGa7QALbAJX4oAww:3:CL:531757:MYCO_Consent_Enablement": {"value": {}},
}

MOCK_REV_REG_DEFS = {
    "TUku9MDGa7QALbAJX4oAww:3:TUku9MDGa7QALbAJX4oAww:3:CL:18:tag:CL_ACCUM:0": {
        "txnTime": 1500000000
    }
}

MOCK_CRED = {
    "schema_id": "Sc886XPwD1gDcHwmmLDeR2:2:degree schema:45.101.94",
    "cred_def_id": "Sc886XPwD1gDcHwmmLDeR2:3:CL:229975:faber.agent.degree_schema",
    "rev_reg_id": None,
    "values": {
        "first_name": {"raw": "Alice", "encoded": "113...335"},
        "last_name": {"raw": "Garcia", "encoded": "532...452"},
        "birthdate_dateint": {"raw": "19981119", "encoded": "19981119"},
    },
    "signature": {
        "p_credential": {
            "m_2": "992...312",
            "a": "548...252",
            "e": "259...199",
            "v": "977...597",
        },
        "r_credential": None,
    },
    "signature_correctness_proof": {"se": "898...935", "c": "935...598"},
    "rev_reg": None,
    "witness": None,
}

MOCK_REV_REG_DEF = {
    "issuerId": "did:web:example.org",
    "revocDefType": "CL_ACCUM",
    "credDefId": "Gs6cQcvrtWoZKsbBhD3dQJ:3:CL:140384:mctc",
    "tag": "MyCustomCredentialDefinition",
    "value": {
        "publicKeys": {"accumKey": {"z": "1 0BB...386"}},
        "maxCredNum": 666,
        "tailsLocation": "https://my.revocations.tails/tailsfile.txt",
        "tailsHash": "91zvq2cFmBZmHCcLqFyzv7bfehHH5rMhdAG5wTjqy2PE",
    },
}
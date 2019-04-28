from guiserver.signals import Signals
from math import isclose

import numpy as np

test_x_svc = [0,0.015847183,0.027477807,0.042585531,0.07489208,0.09940015,0.108102666,0.123971516,0.156437965,0.188777825,0.218226154,0.228005778,0.245309288,0.249807587,0.269873991,0.302350434,0.334733601,0.367113437,0.399416653,0.431669902,0.463979781,0.496352955,0.528732791,0.561119289,0.593532437,0.625912274,0.65829211,0.690671946,0.723048451,0.75]
test_x_hra = [0,0.028809792,0.08273474,0.098016385,0.10654826,0.110085155,0.122650315,0.144257868,0.168441562,0.187247954,0.211993619,0.231153072,0.238708497,0.253331743,0.277402407,0.301670873,0.325798052,0.349769815,0.373798092,0.397911142,0.422038321,0.443443363,0.465013239,0.48945125,0.510375915,0.527952068,0.545528221,0.554151462,0.577854778,0.587870387,0.75]
test_x_ivc = [0,0.038412611,0.060004148,0.081087228,0.10738618,0.133657896,0.159721446,0.185668266,0.211591742,0.236245343,0.260981554,0.287321362,0.313770115,0.340072958,0.366299927,0.392419895,0.418512627,0.444546995,0.470643616,0.496763585,0.522883553,0.549003521,0.575172126,0.600825181,0.62674671,0.653246046,0.679708418,0.70586535,0.727684258,0.75]
test_x_lra = [0,0.018471721,0.049638989,0.082892098,0.103181133,0.128709067,0.151008933,0.177135981,0.223846771,0.26273566,0.2826625,0.307993975,0.333417902,0.358957393,0.384531552,0.410244387,0.429832366,0.449512797,0.475595434,0.501516283,0.527217561,0.552722383,0.571616983,0.597087135,0.622776857,0.648478136,0.674156302,0.699788243,0.725558859,0.75]
test_x_mra = [0,0.029839203,0.048222888,0.06223118,0.079589233,0.093365969,0.103983759,0.122807616,0.143170417,0.154703251,0.166606574,0.199053704,0.212482707,0.230777389,0.254126652,0.271533464,0.293305692,0.323907488,0.353137036,0.382373897,0.41158516,0.440701344,0.469872381,0.493506882,0.50983491,0.529070168,0.555559789,0.582018325,0.611291755,0.628775362,0.75]
test_x_pa  = [0,0.014205258,0.029814629,0.043022557,0.063434811,0.089502762,0.106660759,0.113865084,0.124671571,0.147485266,0.175101844,0.19558011,0.212154696,0.235359116,0.26519337,0.301177527,0.332396268,0.363615008,0.394833749,0.426052489,0.454869788,0.483687087,0.514905827,0.546124568,0.577343309,0.608562049,0.63978079,0.67099953,0.702218271,0.719028362,0.75]
test_x_rv  = [0,0.032484879,0.095802536,0.133747812,0.162716265,0.191778761,0.214170877,0.227896995,0.238729978,0.246676501,0.254701773,0.260719615,0.264718727,0.287618921,0.328671662,0.353669293,0.382573377,0.411504851,0.440457326,0.468325664,0.496156372,0.524997912,0.553928473,0.58292523,0.612018313,0.641163439,0.6691612,0.696924571,0.725862894,0.75]
test_x_rvw = [0,0.012008895,0.058487769,0.079781319,0.158450704,0.26675315,0.326295315,0.329110946,0.330216342,0.337036425,0.339852056,0.34098526,0.351430903,0.366318985,0.381120166,0.395886585,0.410653004,0.425384663,0.44014413,0.45496269,0.467434892,0.47626763,0.48515251,0.492817282,0.501097323,0.509311317,0.518189244,0.533115564,0.550685693,0.563806523,0.75]
test_x_rip = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]

test_y_svc = [-0.0858943180000000,-0.146472741000000,-0.183285430000000,-0.235787398000000,-0.263489366000000,-0.184020913000000,-0.127238558000000,-0.0817422360000000,-0.0518183770000000,-0.0675149640000000,-0.152735249000000,-0.240602349000000,-0.117794216000000,-0.0588105240000000,-0.0179166150000000,0.0156088590000000,0.0155192660000000,0.0142291360000000,-0.0146733700000000,-0.0615839480000000,-0.0880853780000000,-0.0917765840000000,-0.0930667150000000,-0.0919557690000000,-0.0812405190000000,-0.0825306490000000,-0.0838207800000000,-0.0851109100000000,-0.0876015790000000,-0.0858943180000000]
test_y_hra = [-0.293132306000000,-1.46783220400000,-0.528296556000000,-0.420089244000000,-0.327709260000000,-0.258266502000000,-0.190605535000000,-0.122850376000000,-0.113219284000000,-0.0974318070000000,-1.47842404000000,0.0655255380000000,0.0125683670000000,-0.0466807670000000,-0.0520575380000000,-0.0311705500000000,-0.0290433900000000,-0.0475520390000000,-0.0585567580000000,-0.0583055800000000,-0.0561784200000000,-0.0153123470000000,0.0474401910000000,0.0908389720000000,0.0679216320000000,0.000574636000000000,-0.0667723590000000,-0.122332322000000,-0.176484644000000,-0.293132306000000,-0.293132306000000]
test_y_ivc = [0.0315906450000000,-0.349402053000000,0.000158747000000000,-0.0101613100000000,-0.0268878920000000,-0.0412171630000000,-0.0372241260000000,-0.0229568970000000,-0.00663483000000000,0.0393854160000000,0.0781346960000000,0.0578121460000000,0.0279003510000000,0.0108312960000000,0.000440465000000000,-0.000532357000000000,0.000892132000000000,0.00745371700000000,0.00853573400000000,0.00756291200000000,0.00659009000000000,0.00561726800000000,0.000363532000000000,0.0404874770000000,0.0569807800000000,0.0226168360000000,-0.00849361500000000,-0.0127199310000000,0.0365842770000000,0.0315906450000000]
test_y_lra = [-0.211672832000000,-0.0239416360000000,0.387279079000000,-0.575524044000000,-0.378049360000000,-0.346018589000000,-0.311343257000000,0.0250719280000000,-1.85090423300000,-0.324290999000000,-0.294745674000000,-0.227486976000000,-0.176806127000000,-0.146847587000000,-0.123105741000000,-0.124230666000000,-0.179470424000000,-0.251288029000000,-0.318724347000000,-0.357149430000000,-0.356202124000000,-0.320026892000000,-0.250932790000000,-0.208540864000000,-0.205521328000000,-0.204574022000000,-0.199482255000000,-0.186101563000000,-0.197587643000000,-0.211672832000000]
test_y_mra = [0.0246121850000000,0.793750000000000,-1.81250000000000,-0.304473921000000,-0.223778477000000,-0.113830935000000,-0.0283442000000000,0.0510903780000000,0.0990032970000000,0.131250000000000,0.206250000000000,-1.21875000000000,0.225000000000000,0.164568345000000,0.187263939000000,0.247785522000000,0.317763602000000,0.365802608000000,0.376393885000000,0.383959083000000,0.402115558000000,0.459611061000000,0.494410971000000,0.399089478000000,0.300741906000000,0.209959532000000,0.143764051000000,0.0904294060000000,0.0828642090000000,0.0246121850000000,0.0246121850000000]
test_y_pa  = [-0.0751202990000000,-0.122996237000000,-0.205128106000000,-0.271352768000000,-0.356497242000000,-0.334031367000000,-0.270456262000000,-0.183605201000000,-0.103376932000000,-0.0209819380000000,0.000299820000000000,0.0212974510000000,0.482311531000000,-0.483559080000000,-0.0376047050000000,0.0316340150000000,0.0640368410000000,0.0692508890000000,0.0641287080000000,0.0250767290000000,-0.0301430880000000,-0.106893311000000,-0.145271188000000,-0.143652350000000,-0.122035155000000,-0.0810937050000000,-0.0390287510000000,-0.0286465880000000,-0.0261289480000000,-0.0751202990000000,-0.0751202990000000]
test_y_rv  = [-0.117908552000000,-3.12627011000000,0.247142252000000,0.239100745000000,0.238811490000000,0.273237778000000,0.340558250000000,0.417023558000000,0.494887033000000,0.576613311000000,0.687409641000000,0.770096117000000,0.820501817000000,1.05524978800000,0.209674005000000,0.148765380000000,0.124714517000000,0.110774976000000,0.104587450000000,0.0546580320000000,-0.00916241800000000,-0.0563008020000000,-0.0705773870000000,-0.0604182740000000,-0.0147010080000000,0.0502277710000000,0.0480743540000000,-0.0406030990000000,-0.0520148090000000,-0.117908552000000]
test_y_rvw = [-0.257690882000000,0.910952557000000,-2.67707561200000,2.57565789500000,2.57857672300000,2.56245366900000,0.357134202000000,0.302889858000000,0.259363450000000,0.219672325000000,0.165427981000000,0.117660747000000,0.0877808790000000,0.0681844360000000,0.0618405760000000,0.0607977500000000,0.0597549240000000,0.0640131310000000,0.0640305110000000,0.0550361350000000,0.0287221540000000,-0.00528267200000000,-0.0472390470000000,-0.0906988290000000,-0.134202063000000,-0.167633334000000,-0.208529502000000,-0.233957082000000,-0.237259081000000,-0.257690882000000,-0.257690882000000]
test_y_rip = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

test_x_svc_2 = [0,0.00485416990894139,0.0236306713584848,0.0561119371270920,0.0834862237547895,0.102784667930097,0.127411623158902,0.160050647665299,0.187077531634941,0.201010860908194,0.217597829177827,0.228904301958973,0.237435925594225,0.247006928626518,0.274397997520750,0.307110865685804,0.339736463817004,0.372308356447419,0.404843327716812,0.437274245749201,0.467048460181120,0.502428102430503,0.535110761017211,0.567783350056677,0.600459296860709,0.633091607711200,0.665717204905785,0.698342803036985,0.730968401168185,0.750000000000000]
test_x_hra_2 = [0,0.0338781810000000,0.0841118000000000,0.0968747620000000,0.103326887000000,0.106764880000000,0.111589374000000,0.125979967000000,0.144573389000000,0.164840338000000,0.183728838000000,0.214739650000000,0.233804954000000,0.246931403000000,0.271350576000000,0.295449497000000,0.319717963000000,0.367746261000000,0.391816925000000,0.415944104000000,0.437217277000000,0.457200025000000,0.477314642000000,0.501540722000000,0.522234617000000,0.538383767000000,0.545518781000000,0.560184413000000,0.583859472000000,0.590381045000000]
test_x_ivc_2 = [0,0.0388446210140051,0.0658823035915392,0.0915060311175774,0.117777698055762,0.143917014878944,0.170048545766900,0.196150880868282,0.222054690306986,0.247600373194718,0.273362100589562,0.299552021089967,0.326164297695388,0.352595564541517,0.378822465783374,0.404907284001020,0.430920088690096,0.457004906907743,0.483136437795699,0.509312734379983,0.535562992447168,0.561694523335124,0.587767663630281,0.613400931917038,0.639341722097192,0.665724330279380,0.692247074511796,0.718357195548404,0.735850685204651,0.750000000000000]
test_x_lra_2 = [0,0.0514110491834551,0.0896741445965171,0.0924735272554023,0.107346968734233,0.120329680097311,0.145501178887230,0.172810417331540,0.213728197238617,0.263486606287522,0.292399934996327,0.304767699747520,0.330019508465377,0.355454883148042,0.380901731369617,0.406451835628062,0.432208450991365,0.448431103910201,0.467965593544499,0.478826586739371,0.503259997480046,0.528580643555816,0.553775088454668,0.579095734530438,0.604542581783128,0.630046794792592,0.655562479403195,0.681078164982684,0.706593850562173,0.750000000000000]
test_x_mra_2 = [0,0.0119939580000000,0.0345468280000000,0.0598942600000000,0.0709818730000000,0.0807970180000000,0.0923528000000000,0.0980255560000000,0.112369720000000,0.138521077000000,0.161821582000000,0.173655589000000,0.205906344000000,0.221933535000000,0.243612874000000,0.270769573000000,0.301768447000000,0.330880974000000,0.360073953000000,0.389329098000000,0.418554989000000,0.444790455000000,0.467809668000000,0.488717361000000,0.502009063000000,0.518374765000000,0.539028593000000,0.565529184000000,0.596290970000000,0.621148702000000,0.750000000000000]
test_x_pa_2  = [0,0.0364640890000000,0.0629834260000000,0.118328982000000,0.139941957000000,0.161554931000000,0.174762859000000,0.205524862000000,0.222099448000000,0.245303868000000,0.284028451000000,0.305641425000000,0.327254400000000,0.348867374000000,0.370480348000000,0.392093322000000,0.413706296000000,0.435319271000000,0.456932245000000,0.478545219000000,0.500158193000000,0.521771168000000,0.543384142000000,0.564997116000000,0.586610090000000,0.608223064000000,0.629836039000000,0.651449013000000,0.673061987000000,0.702762431000000,0.750000000000000]
test_x_rv_2  = [0,0.0661263443522927,0.0994167549419504,0.121734432231407,0.147802543125558,0.173626201934579,0.196442011880896,0.210731095764082,0.217633798122158,0.224440647765597,0.232149993213508,0.238073249244395,0.270868050373680,0.335549694839250,0.359250475875206,0.385395248901868,0.411487949635269,0.437733975504962,0.464120308001995,0.490497960912215,0.516667323778128,0.542871402377483,0.568875868776803,0.594803673043614,0.620676511531137,0.646873357722328,0.673362388498501,0.699554894896285,0.723881467868302,0.750000000000000]
test_x_rvw_2 = [0,0.0119532990000000,0.0719977770000000,0.0797257230000000,0.125815419000000,0.168402521000000,0.217605634000000,0.276593774000000,0.333691624000000,0.340335031000000,0.340668736000000,0.347071689000000,0.354763575000000,0.368571289000000,0.383455895000000,0.398253600000000,0.413040875000000,0.427807295000000,0.442632808000000,0.457486129000000,0.472370735000000,0.486088767000000,0.497436802000000,0.503875211000000,0.510331348000000,0.515891350000000,0.526813216000000,0.540543762000000,0.555397083000000,0.567822358000000,0.750000000000000]
test_x_rip_2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]

test_y_svc_2 = [-0.0936325450000000,-0.156569804000000,-0.248563273000000,-0.301476541000000,-0.235921787000000,-0.141231586000000,-0.0857738940000000,-0.0822618720000000,-0.140962809000000,-0.197877515000000,-0.265200088000000,-0.221202742000000,-0.169688260000000,-0.101909484000000,-0.0303520390000000,-0.000428180000000000,-0.00171831000000000,-0.0222170500000000,-0.0559217080000000,-0.126843047000000,-0.175446921000000,-0.164238912000000,-0.145119896000000,-0.129602493000000,-0.112884552000000,-0.111773607000000,-0.113063737000000,-0.114353868000000,-0.115643998000000,-0.0936325450000000]
test_y_hra_2 = [-0.299382797000000,-1.46777989900000,-0.511775349000000,-0.417850623000000,-0.361508347000000,-0.305197467000000,-0.224861450000000,-0.154930465000000,-0.0872067040000000,-0.0789157100000000,-0.0905505060000000,-1.45339592500000,0.0780526710000000,-0.0223620650000000,-0.0615002460000000,-0.0631250510000000,-0.0422380630000000,-0.0679994660000000,-0.0733762370000000,-0.0712490760000000,-0.0478921760000000,0.00421409500000000,0.0738295380000000,0.0890885780000000,0.0355301860000000,-0.0212019390000000,-0.0742762900000000,-0.127897476000000,-0.185801763000000,-0.299382797000000,-0.299382797000000]
test_y_ivc_2 = [0.0316964760000000,-0.385808022000000,-0.0145518040000000,-0.0169462470000000,-0.0302480990000000,-0.0319058670000000,-0.0328786890000000,-0.0312829630000000,-0.0122211110000000,0.0383482610000000,0.0699103790000000,0.0638004610000000,0.0205322170000000,-0.00681103000000000,-0.0161744420000000,-0.0130375870000000,-0.00356498100000000,-0.000428126000000000,-0.00140094800000000,-0.00631221000000000,-0.0177304610000000,-0.0187032830000000,-0.0145390090000000,0.0283247200000000,0.0441330780000000,0.0210707440000000,-0.0143206200000000,-0.0134098400000000,0.00692362900000000,0.0316964760000000]
test_y_lra_2 = [-0.255034936000000,0.459103987000000,-0.573549553000000,-0.502975286000000,-0.423662124000000,-0.348564473000000,-0.285450238000000,0.0319564320000000,-1.85861076900000,-0.345972051000000,-0.313158926000000,-0.242229420000000,-0.193620801000000,-0.178167879000000,-0.164787187000000,-0.170056574000000,-0.212626120000000,-0.261767598000000,-0.332894460000000,-0.373944369000000,-0.369582816000000,-0.333407584000000,-0.274437810000000,-0.238262577000000,-0.224881886000000,-0.221862349000000,-0.220915044000000,-0.219967738000000,-0.219020433000000,-0.255034936000000]
test_y_mra_2 = [0.0250000000000000,0.0625000000000000,0.731250000000000,-1.75625000000000,-0.343750000000000,-0.259082734000000,-0.198561151000000,-0.124800472000000,-0.00753990600000000,0.0662207730000000,0.109090228000000,0.175000000000000,-1.16875000000000,0.200000000000000,0.160029227000000,0.221307329000000,0.306794065000000,0.365802608000000,0.391524281000000,0.391524281000000,0.403628597000000,0.442589366000000,0.468750000000000,0.424306805000000,0.318750000000000,0.257872452000000,0.185372639000000,0.114638040000000,0.0964815650000000,0.0250000000000000,0.0250000000000000]
test_y_pa_2  = [-0.0743183030000000,-0.248797006000000,-0.375690608000000,-0.0613794990000000,-0.0310745690000000,-0.0228402350000000,-0.0211259450000000,0.418062734000000,-0.524148993000000,-0.0222776690000000,-0.00841939200000000,0.00435888800000000,0.0119440860000000,0.0162836090000000,0.0102369690000000,-0.0113889170000000,-0.0411289920000000,-0.0786586890000000,-0.107749629000000,-0.124182433000000,-0.137044993000000,-0.139196822000000,-0.136155570000000,-0.109096316000000,-0.0817124940000000,-0.0614691590000000,-0.0499891490000000,-0.0469478970000000,-0.0471523210000000,-0.0743183030000000,-0.0743183030000000]
test_y_rv_2  = [-0.506447874000000,-3.60606389900000,-0.184851119000000,-0.190933760000000,-0.188366021000000,-0.154623872000000,-0.0937591470000000,-0.0148850360000000,0.0553932770000000,0.137895402000000,0.224124929000000,0.300489323000000,0.617003550000000,-0.248408373000000,-0.300402058000000,-0.307610910000000,-0.308179059000000,-0.328300389000000,-0.366314724000000,-0.403222275000000,-0.413567014000000,-0.428338889000000,-0.417654736000000,-0.397193992000000,-0.369723618000000,-0.383573173000000,-0.434684449000000,-0.447980612000000,-0.460959497000000,-0.506447874000000]
test_y_rvw_2 = [-0.248517420000000,0.928604522000000,-2.72817828000000,2.59330985900000,2.56463120800000,2.57009822100000,2.56662342500000,2.57093217200000,0.363510007000000,0.287960062000000,0.237070143000000,0.198468192000000,0.150873603000000,0.108463599000000,0.0893972590000000,0.0835835030000000,0.0793600570000000,0.0783172310000000,0.0682626480000000,0.0539672380000000,0.0349008990000000,0.00616756000000000,-0.0362806810000000,-0.0802896860000000,-0.127002217000000,-0.162100562000000,-0.202081360000000,-0.232723071000000,-0.247018480000000,-0.248517420000000,-0.248517420000000]
test_y_rip_2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


test_x_svc_20 = [0,0.0170480540000000,0.0295600270000000,0.0458125870000000,0.0805672690000000,0.106932518000000,0.116294495000000,0.133365858000000,0.168292557000000,0.203083075000000,0.234762946000000,0.245283653000000,0.263898392000000,0.268737564000000,0.290324565000000,0.325262015000000,0.360099121000000,0.394932644000000,0.429683741000000,0.464381084000000,0.499139349000000,0.533965704000000,0.568799227000000,0.603639917000000,0.638509276000000,0.673342799000000,0.708176322000000,0.743009845000000,0.777839784000000,0.806833674000000,3]
test_x_hra_20 = [0,0.0288097920000000,0.0827347400000000,0.0980163850000000,0.106548260000000,0.110085155000000,0.122650315000000,0.144257868000000,0.168441562000000,0.187247954000000,0.211993619000000,0.231153072000000,0.238708497000000,0.253331743000000,0.277402407000000,0.301670873000000,0.325798052000000,0.349769815000000,0.373798092000000,0.397911142000000,0.422038321000000,0.443443363000000,0.465013239000000,0.489451250000000,0.510375915000000,0.527952068000000,0.545528221000000,0.554151462000000,0.577854778000000,0.587870387000000,3]
test_x_ivc_20 = [0,0.0391999160000000,0.0612339930000000,0.0827491920000000,0.109587167000000,0.136397348000000,0.162995096000000,0.189473722000000,0.215928525000000,0.241087427000000,0.266330631000000,0.293210299000000,0.320201146000000,0.347043092000000,0.373807609000000,0.400462932000000,0.427090460000000,0.453658428000000,0.480289926000000,0.506945249000000,0.533600572000000,0.560255895000000,0.586960852000000,0.613139691000000,0.639592508000000,0.666634974000000,0.693639719000000,0.720332763000000,0.742598872000000,0.765371997000000,3]
test_x_lra_20 = [0,0.0189272510000000,0.0508631320000000,0.0849362930000000,0.105725674000000,0.131883150000000,0.154732951000000,0.181504316000000,0.229367037000000,0.269214961000000,0.289633215000000,0.315589388000000,0.341640292000000,0.367809610000000,0.394014451000000,0.420361388000000,0.440432425000000,0.460598193000000,0.487324052000000,0.513884133000000,0.540219228000000,0.566353022000000,0.585713580000000,0.611811849000000,0.638135103000000,0.664470199000000,0.690781612000000,0.717045660000000,0.743451803000000,0.768495685000000,3]
test_x_mra_20 = [0,0.0298392030000000,0.0482228880000000,0.0622311800000000,0.0795892330000000,0.0933659690000000,0.103983759000000,0.122807616000000,0.143170417000000,0.154703251000000,0.166606574000000,0.199053704000000,0.212482707000000,0.230777389000000,0.254126652000000,0.271533464000000,0.293305692000000,0.323907488000000,0.353137036000000,0.382373897000000,0.411585160000000,0.440701344000000,0.469872381000000,0.493506882000000,0.509834910000000,0.529070168000000,0.555559789000000,0.582018325000000,0.611291755000000,0.628775362000000,3]
test_x_pa_20  = [0,0.0142052580000000,0.0298146290000000,0.0430225570000000,0.0634348110000000,0.0895027620000000,0.106660759000000,0.113865084000000,0.124671571000000,0.147485266000000,0.175101844000000,0.195580110000000,0.212154696000000,0.235359116000000,0.265193370000000,0.301177527000000,0.332396268000000,0.363615008000000,0.394833749000000,0.426052489000000,0.454869788000000,0.483687087000000,0.514905827000000,0.546124568000000,0.577343309000000,0.608562049000000,0.639780790000000,0.670999530000000,0.702218271000000,0.719028362000000,3]
test_x_rv_20  = [0,0.0357959360000000,0.105567316000000,0.147380207000000,0.179301302000000,0.211326025000000,0.236000483000000,0.251125651000000,0.263062797000000,0.271819279000000,0.280662536000000,0.287293753000000,0.291700479000000,0.316934801000000,0.362171888000000,0.389717430000000,0.421567595000000,0.453447942000000,0.485351430000000,0.516060280000000,0.546727664000000,0.578508910000000,0.610388251000000,0.642340535000000,0.674398963000000,0.706514738000000,0.737366202000000,0.767959386000000,0.799847280000000,0.826444587000000,3]
test_x_rvw_20 = [0,0.0120088950000000,0.0584877690000000,0.0797813190000000,0.158450704000000,0.266753150000000,0.326295315000000,0.329110946000000,0.330216342000000,0.337036425000000,0.339852056000000,0.340985260000000,0.351430903000000,0.366318985000000,0.381120166000000,0.395886585000000,0.410653004000000,0.425384663000000,0.440144130000000,0.454962690000000,0.467434892000000,0.476267630000000,0.485152510000000,0.492817282000000,0.501097323000000,0.509311317000000,0.518189244000000,0.533115564000000,0.550685693000000,0.563806523000000,3]
test_x_rip_20 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]

test_y_svc_20 = [-0.0858943180000000,-0.146472741000000,-0.183285430000000,-0.235787398000000,-0.263489366000000,-0.184020913000000,-0.127238558000000,-0.0817422360000000,-0.0518183770000000,-0.0675149640000000,-0.152735249000000,-0.240602349000000,-0.117794216000000,-0.0588105240000000,-0.0179166150000000,0.0156088590000000,0.0155192660000000,0.0142291360000000,-0.0146733700000000,-0.0615839480000000,-0.0880853780000000,-0.0917765840000000,-0.0930667150000000,-0.0919557690000000,-0.0812405190000000,-0.0825306490000000,-0.0838207800000000,-0.0851109100000000,-0.0876015790000000,-0.0858943180000000,-0.0858943180000000]
test_y_hra_20 = [-0.293132306000000,-1.46783220400000,-0.528296556000000,-0.420089244000000,-0.327709260000000,-0.258266502000000,-0.190605535000000,-0.122850376000000,-0.113219284000000,-0.0974318070000000,-1.47842404000000,0.0655255380000000,0.0125683670000000,-0.0466807670000000,-0.0520575380000000,-0.0311705500000000,-0.0290433900000000,-0.0475520390000000,-0.0585567580000000,-0.0583055800000000,-0.0561784200000000,-0.0153123470000000,0.0474401910000000,0.0908389720000000,0.0679216320000000,0.000574636000000000,-0.0667723590000000,-0.122332322000000,-0.176484644000000,-0.293132306000000,-0.293132306000000]
test_y_ivc_20 = [0.0315906450000000,-0.349402053000000,0.000158747000000000,-0.0101613100000000,-0.0268878920000000,-0.0412171630000000,-0.0372241260000000,-0.0229568970000000,-0.00663483000000000,0.0393854160000000,0.0781346960000000,0.0578121460000000,0.0279003510000000,0.0108312960000000,0.000440465000000000,-0.000532357000000000,0.000892132000000000,0.00745371700000000,0.00853573400000000,0.00756291200000000,0.00659009000000000,0.00561726800000000,0.000363532000000000,0.0404874770000000,0.0569807800000000,0.0226168360000000,-0.00849361500000000,-0.0127199310000000,0.0365842770000000,0.0315906450000000,0.0315906450000000]
test_y_lra_20 = [-0.211672832000000,-0.0239416360000000,0.387279079000000,-0.575524044000000,-0.378049360000000,-0.346018589000000,-0.311343257000000,0.0250719280000000,-1.85090423300000,-0.324290999000000,-0.294745674000000,-0.227486976000000,-0.176806127000000,-0.146847587000000,-0.123105741000000,-0.124230666000000,-0.179470424000000,-0.251288029000000,-0.318724347000000,-0.357149430000000,-0.356202124000000,-0.320026892000000,-0.250932790000000,-0.208540864000000,-0.205521328000000,-0.204574022000000,-0.199482255000000,-0.186101563000000,-0.197587643000000,-0.211672832000000,-0.211672832000000]
test_y_mra_20 = [0.0246121850000000,0.793750000000000,-1.81250000000000,-0.304473921000000,-0.223778477000000,-0.113830935000000,-0.0283442000000000,0.0510903780000000,0.0990032970000000,0.131250000000000,0.206250000000000,-1.21875000000000,0.225000000000000,0.164568345000000,0.187263939000000,0.247785522000000,0.317763602000000,0.365802608000000,0.376393885000000,0.383959083000000,0.402115558000000,0.459611061000000,0.494410971000000,0.399089478000000,0.300741906000000,0.209959532000000,0.143764051000000,0.0904294060000000,0.0828642090000000,0.0246121850000000,0.0246121850000000]
test_y_pa_20  = [-0.0751202990000000,-0.122996237000000,-0.205128106000000,-0.271352768000000,-0.356497242000000,-0.334031367000000,-0.270456262000000,-0.183605201000000,-0.103376932000000,-0.0209819380000000,0.000299820000000000,0.0212974510000000,0.482311531000000,-0.483559080000000,-0.0376047050000000,0.0316340150000000,0.0640368410000000,0.0692508890000000,0.0641287080000000,0.0250767290000000,-0.0301430880000000,-0.106893311000000,-0.145271188000000,-0.143652350000000,-0.122035155000000,-0.0810937050000000,-0.0390287510000000,-0.0286465880000000,-0.0261289480000000,-0.0751202990000000,-0.0751202990000000]
test_y_rv_20  = [-0.117908552000000,-3.12627011000000,0.247142252000000,0.239100745000000,0.238811490000000,0.273237778000000,0.340558250000000,0.417023558000000,0.494887033000000,0.576613311000000,0.687409641000000,0.770096117000000,0.820501817000000,1.05524978800000,0.209674005000000,0.148765380000000,0.124714517000000,0.110774976000000,0.104587450000000,0.0546580320000000,-0.00916241800000000,-0.0563008020000000,-0.0705773870000000,-0.0604182740000000,-0.0147010080000000,0.0502277710000000,0.0480743540000000,-0.0406030990000000,-0.0520148090000000,-0.117908552000000,-0.117908552000000]
test_y_rvw_20 = [-0.257690882000000,0.910952557000000,-2.67707561200000,2.57565789500000,2.57857672300000,2.56245366900000,0.357134202000000,0.302889858000000,0.259363450000000,0.219672325000000,0.165427981000000,0.117660747000000,0.0877808790000000,0.0681844360000000,0.0618405760000000,0.0607977500000000,0.0597549240000000,0.0640131310000000,0.0640305110000000,0.0550361350000000,0.0287221540000000,-0.00528267200000000,-0.0472390470000000,-0.0906988290000000,-0.134202063000000,-0.167633334000000,-0.208529502000000,-0.233957082000000,-0.237259081000000,-0.257690882000000,-0.257690882000000]
test_y_rip_20 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

test_x_svc_140 = [0,0.00905553287199917,0.0157016041945716,0.0243345890111459,0.0427954740662306,0.0568000859121307,0.0617729520510108,0.0708408661259152,0.0893931226418155,0.107873042953124,0.124700659361495,0.130289016136712,0.140176735926794,0.142747192421081,0.154213709195569,0.172771676394572,0.191276343176383,0.209779106751277,0.228238087537092,0.246668515438572,0.265131303700573,0.283630259799281,0.302133023374176,0.320639593894080,0.339161392725198,0.357664156300093,0.376166919874988,0.394669683449882,0.413170543286684,0.428571428571429]
test_x_hra_140 = [0,0.0288097920000000,0.0827347400000000,0.0980163850000000,0.106548260000000,0.110085155000000,0.122650315000000,0.144257868000000,0.168441562000000,0.187247954000000,0.211993619000000,0.231153072000000,0.238708497000000,0.253331743000000,0.277402407000000,0.301670873000000,0.325798052000000,0.349769815000000,0.373798092000000,0.397911142000000,0.422038321000000,0.443443363000000,0.465013239000000,0.489451250000000,0.510375915000000,0.527952068000000,0.545528221000000,0.554151462000000,0.577854778000000,0.587870387000000,3]
test_x_ivc_140 = [0,0.0391999160000000,0.0612339930000000,0.0827491920000000,0.109587167000000,0.136397348000000,0.162995096000000,0.189473722000000,0.215928525000000,0.241087427000000,0.266330631000000,0.293210299000000,0.320201146000000,0.347043092000000,0.373807609000000,0.400462932000000,0.427090460000000,0.453658428000000,0.480289926000000,0.506945249000000,0.533600572000000,0.560255895000000,0.586960852000000,0.613139691000000,0.639592508000000,0.666634974000000,0.693639719000000,0.720332763000000,0.742598872000000,0.765371997000000,3]
test_x_lra_140 = [0,0.0189272510000000,0.0508631320000000,0.0849362930000000,0.105725674000000,0.131883150000000,0.154732951000000,0.181504316000000,0.229367037000000,0.269214961000000,0.289633215000000,0.315589388000000,0.341640292000000,0.367809610000000,0.394014451000000,0.420361388000000,0.440432425000000,0.460598193000000,0.487324052000000,0.513884133000000,0.540219228000000,0.566353022000000,0.585713580000000,0.611811849000000,0.638135103000000,0.664470199000000,0.690781612000000,0.717045660000000,0.743451803000000,0.768495685000000,3]
test_x_mra_140 = [0,0.0298392030000000,0.0482228880000000,0.0622311800000000,0.0795892330000000,0.0933659690000000,0.103983759000000,0.122807616000000,0.143170417000000,0.154703251000000,0.166606574000000,0.199053704000000,0.212482707000000,0.230777389000000,0.254126652000000,0.271533464000000,0.293305692000000,0.323907488000000,0.353137036000000,0.382373897000000,0.411585160000000,0.440701344000000,0.469872381000000,0.493506882000000,0.509834910000000,0.529070168000000,0.555559789000000,0.582018325000000,0.611291755000000,0.628775362000000,3]
test_x_pa_140 = [0,0.0142052580000000,0.0298146290000000,0.0430225570000000,0.0634348110000000,0.0895027620000000,0.106660759000000,0.113865084000000,0.124671571000000,0.147485266000000,0.175101844000000,0.195580110000000,0.212154696000000,0.235359116000000,0.265193370000000,0.301177527000000,0.332396268000000,0.363615008000000,0.394833749000000,0.426052489000000,0.454869788000000,0.483687087000000,0.514905827000000,0.546124568000000,0.577343309000000,0.608562049000000,0.639780790000000,0.670999530000000,0.702218271000000,0.719028362000000,3]
test_x_rv_140 = [0,0.0357959360000000,0.105567316000000,0.147380207000000,0.179301302000000,0.211326025000000,0.236000483000000,0.251125651000000,0.263062797000000,0.271819279000000,0.280662536000000,0.287293753000000,0.291700479000000,0.316934801000000,0.362171888000000,0.389717430000000,0.421567595000000,0.453447942000000,0.485351430000000,0.516060280000000,0.546727664000000,0.578508910000000,0.610388251000000,0.642340535000000,0.674398963000000,0.706514738000000,0.737366202000000,0.767959386000000,0.799847280000000,0.826444587000000,3]
test_x_rvw_140 = [0,0.0120088950000000,0.0584877690000000,0.0797813190000000,0.158450704000000,0.266753150000000,0.326295315000000,0.329110946000000,0.330216342000000,0.337036425000000,0.339852056000000,0.340985260000000,0.351430903000000,0.366318985000000,0.381120166000000,0.395886585000000,0.410653004000000,0.425384663000000,0.440144130000000,0.454962690000000,0.467434892000000,0.476267630000000,0.485152510000000,0.492817282000000,0.501097323000000,0.509311317000000,0.518189244000000,0.533115564000000,0.550685693000000,0.563806523000000,3]
test_x_rip_140 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]

test_y_svc_140 = [-0.0858943180000000,-0.146472741000000,-0.183285430000000,-0.235787398000000,-0.263489366000000,-0.184020913000000,-0.127238558000000,-0.0817422360000000,-0.0518183770000000,-0.0675149640000000,-0.152735249000000,-0.240602349000000,-0.117794216000000,-0.0588105240000000,-0.0179166150000000,0.0156088590000000,0.0155192660000000,0.0142291360000000,-0.0146733700000000,-0.0615839480000000,-0.0880853780000000,-0.0917765840000000,-0.0930667150000000,-0.0919557690000000,-0.0812405190000000,-0.0825306490000000,-0.0838207800000000,-0.0851109100000000,-0.0876015790000000,-0.0858943180000000]
test_y_hra_140 = [-0.293132306000000,-1.46783220400000,-0.528296556000000,-0.420089244000000,-0.327709260000000,-0.258266502000000,-0.190605535000000,-0.122850376000000,-0.113219284000000,-0.0974318070000000,-1.47842404000000,0.0655255380000000,0.0125683670000000,-0.0466807670000000,-0.0520575380000000,-0.0311705500000000,-0.0290433900000000,-0.0475520390000000,-0.0585567580000000,-0.0583055800000000,-0.0561784200000000,-0.0153123470000000,0.0474401910000000,0.0908389720000000,0.0679216320000000,0.000574636000000000,-0.0667723590000000,-0.122332322000000,-0.176484644000000,-0.293132306000000,-0.293132306000000]
test_y_ivc_140 = [0.0315906450000000,-0.349402053000000,0.000158747000000000,-0.0101613100000000,-0.0268878920000000,-0.0412171630000000,-0.0372241260000000,-0.0229568970000000,-0.00663483000000000,0.0393854160000000,0.0781346960000000,0.0578121460000000,0.0279003510000000,0.0108312960000000,0.000440465000000000,-0.000532357000000000,0.000892132000000000,0.00745371700000000,0.00853573400000000,0.00756291200000000,0.00659009000000000,0.00561726800000000,0.000363532000000000,0.0404874770000000,0.0569807800000000,0.0226168360000000,-0.00849361500000000,-0.0127199310000000,0.0365842770000000,0.0315906450000000,0.0315906450000000]
test_y_lra_140 = [-0.211672832000000,-0.0239416360000000,0.387279079000000,-0.575524044000000,-0.378049360000000,-0.346018589000000,-0.311343257000000,0.0250719280000000,-1.85090423300000,-0.324290999000000,-0.294745674000000,-0.227486976000000,-0.176806127000000,-0.146847587000000,-0.123105741000000,-0.124230666000000,-0.179470424000000,-0.251288029000000,-0.318724347000000,-0.357149430000000,-0.356202124000000,-0.320026892000000,-0.250932790000000,-0.208540864000000,-0.205521328000000,-0.204574022000000,-0.199482255000000,-0.186101563000000,-0.197587643000000,-0.211672832000000,-0.211672832000000]
test_y_mra_140 = [0.0246121850000000,0.793750000000000,-1.81250000000000,-0.304473921000000,-0.223778477000000,-0.113830935000000,-0.0283442000000000,0.0510903780000000,0.0990032970000000,0.131250000000000,0.206250000000000,-1.21875000000000,0.225000000000000,0.164568345000000,0.187263939000000,0.247785522000000,0.317763602000000,0.365802608000000,0.376393885000000,0.383959083000000,0.402115558000000,0.459611061000000,0.494410971000000,0.399089478000000,0.300741906000000,0.209959532000000,0.143764051000000,0.0904294060000000,0.0828642090000000,0.0246121850000000,0.0246121850000000]
test_y_pa_140  = [-0.0751202990000000,-0.122996237000000,-0.205128106000000,-0.271352768000000,-0.356497242000000,-0.334031367000000,-0.270456262000000,-0.183605201000000,-0.103376932000000,-0.0209819380000000,0.000299820000000000,0.0212974510000000,0.482311531000000,-0.483559080000000,-0.0376047050000000,0.0316340150000000,0.0640368410000000,0.0692508890000000,0.0641287080000000,0.0250767290000000,-0.0301430880000000,-0.106893311000000,-0.145271188000000,-0.143652350000000,-0.122035155000000,-0.0810937050000000,-0.0390287510000000,-0.0286465880000000,-0.0261289480000000,-0.0751202990000000,-0.0751202990000000]
test_y_rv_140  = [-0.117908552000000,-3.12627011000000,0.247142252000000,0.239100745000000,0.238811490000000,0.273237778000000,0.340558250000000,0.417023558000000,0.494887033000000,0.576613311000000,0.687409641000000,0.770096117000000,0.820501817000000,1.05524978800000,0.209674005000000,0.148765380000000,0.124714517000000,0.110774976000000,0.104587450000000,0.0546580320000000,-0.00916241800000000,-0.0563008020000000,-0.0705773870000000,-0.0604182740000000,-0.0147010080000000,0.0502277710000000,0.0480743540000000,-0.0406030990000000,-0.0520148090000000,-0.117908552000000,-0.117908552000000]
test_y_rvw_140 = [-0.257690882000000,0.910952557000000,-2.67707561200000,2.57565789500000,2.57857672300000,2.56245366900000,0.357134202000000,0.302889858000000,0.259363450000000,0.219672325000000,0.165427981000000,0.117660747000000,0.0877808790000000,0.0681844360000000,0.0618405760000000,0.0607977500000000,0.0597549240000000,0.0640131310000000,0.0640305110000000,0.0550361350000000,0.0287221540000000,-0.00528267200000000,-0.0472390470000000,-0.0906988290000000,-0.134202063000000,-0.167633334000000,-0.208529502000000,-0.233957082000000,-0.237259081000000,-0.257690882000000,-0.257690882000000]
test_y_rip_140 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

signals = Signals()

def is_close_enough(list_1, list_2, tolerance=1e-4):
    similar = True

    for i in range(min(len(list_1), len(list_2))):
        similar = isclose(list_1[i], list_2[i], abs_tol=tolerance)

    return similar

def test_SVC_V1():
    [x,y] = signals.get_signal('SVC', 80, 0)
    assert is_close_enough(x, test_x_svc)
    assert is_close_enough(y, test_y_svc)
    
def test_SVC_20():
    [x1,y1]=signals.get_signal('SVC', 20, 0)
    assert is_close_enough(x1, test_x_svc_20)
    assert is_close_enough(y1, test_y_svc_20)
    
def test_SVC_V2():
    [x,y] = signals.get_signal('SVC', 80, 1)

    assert is_close_enough(x, test_x_svc_2)
    assert is_close_enough(y, test_y_svc_2)

def test_High_RA_V1():
    [x,y] = signals.get_signal('HRA', 80, 0)

    assert is_close_enough(x, test_x_hra)
    assert is_close_enough(y, test_y_hra)

def test_High_RA_V2():
    [x,y] = signals.get_signal('HRA', 80, 1)

    assert is_close_enough(x, test_x_hra_2)
    assert is_close_enough(y, test_y_hra_2)

def test_IVC_V1():
    [x,y] = signals.get_signal('IVC', 80, 0)

    assert is_close_enough(x, test_x_ivc)
    assert is_close_enough(y, test_y_ivc)

def test_IVC_V2():
    [x,y] = signals.get_signal('IVC', 80, 1)

    assert is_close_enough(x, test_x_ivc_2)
    assert is_close_enough(y, test_y_ivc_2)

def test_Mid_RA_V1():
    [x,y] = signals.get_signal('MRA', 80, 0)

    assert is_close_enough(x, test_x_mra)
    assert is_close_enough(y, test_y_mra)

def test_Mid_RA_V2():
    [x,y] = signals.get_signal('MRA', 80, 1)

    assert is_close_enough(x, test_x_mra_2)
    assert is_close_enough(y, test_y_mra_2)

def test_Low_RA_V1():
    [x,y] = signals.get_signal('LRA', 80, 0)

    assert is_close_enough(x, test_x_lra)
    assert is_close_enough(y, test_y_lra)

def test_Low_RA_V2():
    [x,y] = signals.get_signal('LRA', 80, 1)

    assert is_close_enough(x, test_x_lra_2)
    assert is_close_enough(y, test_y_lra_2)

def test_PA_V1():
    [x,y] = signals.get_signal('PA', 80, 0)

    assert is_close_enough(x, test_x_pa)
    assert is_close_enough(y, test_y_pa)

def test_PA_V2():
    [x,y] = signals.get_signal('PA', 80, 1)

    assert is_close_enough(x, test_x_pa_2)
    assert is_close_enough(y, test_y_pa_2)

def test_RV_V1():
    [x,y] = signals.get_signal('RV', 80, 0)

    assert is_close_enough(x, test_x_rv)
    assert is_close_enough(y, test_y_rv)

def test_RV_V2():
    [x,y] = signals.get_signal('RV', 80, 1)

    assert is_close_enough(x, test_x_rv_2)
    assert is_close_enough(y, test_y_rv_2)

def test_RV_Wall_V1():
    [x,y] = signals.get_signal('RVW', 80, 0)

    assert is_close_enough(x, test_x_rvw)
    assert is_close_enough(y, test_y_rvw)

def test_RV_Wall_V2():
    [x,y] = signals.get_signal('RVW', 80, 1)

    assert is_close_enough(x, test_x_rvw_2)
    assert is_close_enough(y, test_y_rvw_2)

def test_Default_Line():
    [x,y] = signals.get_signal('RIP', 80, 0)

    assert is_close_enough(x, test_x_rip)
    assert is_close_enough(y, test_y_rip)

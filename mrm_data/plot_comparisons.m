clc
clear all
close all

defaults_daniella
names={['Analttic_AE_Data_Norberto_W_SKIN_corrected'] 
 ['Analttic_AE_Data_Norberto_WO_SKIN_corrected']
['AE results from MRM of UM beam model wing 1 W skin']
['AE results from MRM of UM beam model wing 1 WO skin']
['AE results from MRM of Nastran model wing 1']
['AE results from MRM of Nastran model wing 2']
['AE results from MRM of Nastran model wing 1 with weight']
['AE results from MRM of Nastran model wing 2 with weight']
['aeroelastic test and anaysis']
};

leg={    ['MRM, wing1, Ansys, W skin']...
        ,['MRM, wing1, Ansys, W/O skin']...
        ,['MRM, wing1, UM beam, W skin']...
        ,['MRM, wing1, UM beam, W/O skin']...
        ,['MRM, wing1, Nastran, W skin']...
        ,['MRM, wing2, Nastran, W skin']...
        ,['MRM, wing1, Nastran, W skin + Weight']...
        ,['MRM, wing2, Nastran, W skin + Weight']...
        ,['wing1 Test']...
        ,['UMNAST, wing1, W skin']...
        ,['UMNAST, wing1, W/O skin']...
        ,['Sharpy, wing1, W skin']...
        ,['Sharpy, wing1, W/O skin']}

for i=1:length(names)
    
    load(names{i})
    figure(1)
    switch i
        case 1
    plot(Norberto_Static_AE_Data(:,end)/0.55*100,Norberto_nonmached_flutter_Data(:,1,end),'r-','LineWidth',2)
        case 2
    plot(Norberto_Static_AE_Data(:,end)/0.55*100,Norberto_nonmached_flutter_Data(:,1,end),'r:','LineWidth',2)
        case 3
    plot(Norberto_Static_AE_Data(:,end)/0.55*100,Norberto_nonmached_flutter_Data(:,1,end),'m-','LineWidth',2)
        case 4
    plot(Norberto_Static_AE_Data(:,end)/0.55*100,Norberto_nonmached_flutter_Data(:,1,end),'m:','LineWidth',2)
        case 5
    plot(Norberto_Static_AE_Data(:,end)/0.55*100,Norberto_nonmached_flutter_Data(:,1,end),'b-','LineWidth',2)
        case 6
    plot(Norberto_Static_AE_Data(:,end)/0.55*100,Norberto_nonmached_flutter_Data(:,1,end),'b-o','LineWidth',2)
        case 7
    plot(Norberto_Static_AE_Data(:,end)/0.55*100,Norberto_nonmached_flutter_Data(:,1,end),'b--','LineWidth',2)
        case 8
    plot(Norberto_Static_AE_Data(:,end)/0.55*100,Norberto_nonmached_flutter_Data(:,1,end),'b--o','LineWidth',2)
    end              
    hold on
    grid on
    xlabel('deformationn (%span)')
    ylabel('flutter velocity (m/s)')
    xlim([0,50]) 
    legend(leg(1:length(names)-1),'location','EastOutside')    
%     legend('Wing1, Ansys, W skin'...
%         ,'Wing1, Ansys, W/O skin'...
%         ,'wing1, UM beam, W skin'...
%         ,'wing1, UM beam, W/O skin'...
%         ,'wing1, Nastran, W skin'...
%         ,'wing2, Nastran, W skin'...
%         ,'wing1, Nastran, W skin + Weight'...
%         ,'wing2, Nastran, W skin + Weight','location','EastOutside')
    
    figure(2)
    switch i
        case 1
    plot(0.5*1.225*Norberto_Vel_Data.^2,Norberto_Static_AE_Data(:,end)/0.55*100','r-','LineWidth',2)
        case 2
    plot(0.5*1.225*Norberto_Vel_Data.^2,Norberto_Static_AE_Data(:,end)/0.55*100','r:','LineWidth',2)
        case 3
    plot(0.5*1.225*Norberto_Vel_Data.^2,Norberto_Static_AE_Data(:,end)/0.55*100','m-','LineWidth',2)
        case 4
    plot(0.5*1.225*Norberto_Vel_Data.^2,Norberto_Static_AE_Data(:,end)/0.55*100','m:','LineWidth',2)
        case 5
    plot(0.5*1.225*Norberto_Vel_Data.^2,Norberto_Static_AE_Data(:,end)/0.55*100','b-','LineWidth',2)
        case 6
    plot(0.5*1.225*Norberto_Vel_Data.^2,Norberto_Static_AE_Data(:,end)/0.55*100','b-o','LineWidth',2)
        case 7
%     plot(0.5*1.225*Norberto_Vel_Data.^2,Norberto_Static_AE_Data(:,end)','b--','LineWidth',2)
        case 8
%     plot(0.5*1.225*Norberto_Vel_Data.^2,Norberto_Static_AE_Data(:,end)','b--o','LineWidth',2)
       case 9
           plot(AE_TEST_7_DEG_DATA(:,1),AE_TEST_7_DEG_DATA(:,2),'k>','LineWidth',2,'MarkerSize',5)
    end              
    hold on
    grid on
    xlabel('dynamic pressure (Pa)')
    ylabel('deformarion (% span)')
    xlim([0,2500]) 
    legend(leg([1:6,9]),'location','EastOutside')       

    
      
    
end
if 1
UM_NAST_WO_skin=[0.000000000000000000e+00 0.000000000000000000e+00 0.000000000000000000e+00 0.000000000000000000e+00 0.000000000000000000e+00
1.000000000000000000e+00 8.073581351983865749e-05 -6.023792242793035712e-09 8.064272599920428101e-05 -5.397850277866211854e-09
2.000000000000000000e+00 3.230550110356021631e-04 -1.046266995263778199e-07 3.226825526424352574e-04 -1.019997585283149988e-07
3.000000000000000000e+00 7.272930536482845494e-04 -5.379628181811924037e-07 7.264545737476049486e-04 -5.315894647806018725e-07
4.000000000000000000e+00 1.294007893795279772e-03 -1.711487099487207786e-06 1.292516142274830219e-03 -1.699001882071726754e-06
5.000000000000000000e+00 2.023978563543438105e-03 -4.196752457663599500e-06 2.021645442925984384e-03 -4.174915996024708420e-06
6.000000000000000000e+00 2.918203137139740826e-03 -8.735326278541677425e-06 2.914839510102254505e-03 -8.699765789765834256e-06
7.000000000000000000e+00 3.977895154357460362e-03 -1.624381847620259833e-05 3.973310561159773893e-03 -1.618876042597250375e-05
8.000000000000000000e+00 5.204480484595802765e-03 -2.782002792223181586e-05 5.198482927428548818e-03 -2.773802167865824231e-05
9.000000000000000000e+00 6.599592249468699649e-03 -4.475018881777703683e-05 6.591988009197596692e-03 -4.463182001501753149e-05
1.000000000000000000e+01 8.165219081744057306e-03 -6.851989746803344161e-05 8.155812296498863787e-03 -6.835348319200740264e-05
1.100000000000000000e+01 9.903117051133576015e-03 -1.008144407642630469e-04 9.891710010161107805e-03 -1.005857293424616827e-04
1.200000000000000000e+01 1.181562202960084219e-02 -1.435413544442765144e-04 1.180201452649664445e-02 -1.432331849715584582e-04
1.300000000000000000e+01 1.390512183687326112e-02 -1.988345464513097127e-04 1.388911113987330997e-02 -1.984265066937718203e-04
1.400000000000000000e+01 1.617443617709040868e-02 -2.690772909953453862e-04 1.615581655679109579e-02 -2.685453377296864730e-04
1.500000000000000000e+01 1.862576994174302766e-02 -3.568826356490362173e-04 1.860433338896968353e-02 -3.561987527743726289e-04
1.600000000000000000e+01 2.126247738860036554e-02 -4.651656463742215308e-04 2.123801234037428140e-02 -4.642973812775119669e-04
1.700000000000000000e+01 2.408693669788836839e-02 -5.970811841239376250e-04 2.405922916583822652e-02 -5.959912940967093675e-04
1.800000000000000000e+01 2.710275379294908860e-02 -7.561314817294828572e-04 2.707158599802516122e-02 -7.547774016553043808e-04
1.900000000000000000e+01 3.031239045400197993e-02 -9.460701754194777990e-04 3.027754215273199129e-02 -9.444036489719698224e-04
2.000000000000000000e+01 3.371958395497934302e-02 -1.171047703023231357e-03 3.368083103548480395e-02 -1.169014176870430965e-03
2.100000000000000000e+01 3.732675745678618040e-02 -1.435472855045860641e-03 3.728387344831805839e-02 -1.433011101105718943e-03
2.200000000000000000e+01 4.113762386692063761e-02 -1.744202092353153155e-03 4.109037852533112961e-02 -1.741243525861135844e-03
2.300000000000000000e+01 4.515440677481906417e-02 -2.102349254738955509e-03 4.510256779975003322e-02 -2.098817560723387210e-03
2.400000000000000000e+01 4.938020455316595447e-02 -2.515484067965090276e-03 4.932353664513743075e-02 -2.511294510762152044e-03
2.500000000000000000e+01 5.381801397066469927e-02 -2.989581090739767966e-03 5.375627899640951501e-02 -2.984639908911956852e-03
2.600000000000000000e+01 5.846927744358236534e-02 -3.530861258075335130e-03 5.840223622494505190e-02 -3.525065308465191727e-03
2.700000000000000000e+01 6.333676246267158638e-02 -4.146115752782342234e-03 6.326417334372071155e-02 -4.139351645693234438e-03
2.800000000000000000e+01 6.842110990177172059e-02 -4.842304407291497803e-03 6.834273118998626662e-02 -4.834448273097868842e-03
2.900000000000000000e+01 7.372416264028502919e-02 -5.626975612441964536e-03 7.363975131715465305e-02 -5.617892210271424602e-03
3.000000000000000000e+01 7.924544253219648060e-02 -6.507773158846763550e-03 7.915475691386152091e-02 -6.497315754569354951e-03
3.100000000000000000e+01 8.498505572860996782e-02 -7.492838850561622799e-03 8.488785487570121857e-02 -7.480848466567935340e-03
3.200000000000000000e+01 9.094241032040915884e-02 -8.590624593629581085e-03 9.083845488269304269e-02 -8.576929550477618847e-03
3.300000000000000000e+01 9.711459967971115825e-02 -9.809539978297032725e-03 9.700365455331402820e-02 -9.793955978244062166e-03
3.400000000000000000e+01 1.034991441754832264e-01 -1.115841440085085789e-02 1.033809780889244079e-01 -1.114074389448660440e-02
3.500000000000000000e+01 1.100925678761155296e-01 -1.264621169631663378e-02 1.099669545612262933e-01 -1.262624368681897202e-02
3.600000000000000000e+01 1.168887573237243904e-01 -1.428156696003735071e-02 1.167554785403785295e-01 -1.425907751779043053e-02
3.700000000000000000e+01 1.238818516409305875e-01 -1.607336172631934623e-02 1.237406969355487191e-01 -1.604811361074787168e-02
3.800000000000000000e+01 1.310642468258963744e-01 -1.803019026740304565e-02 1.309150155334989352e-01 -1.800193336674005273e-02
3.900000000000000000e+01 1.384275544311488748e-01 -2.016050847753847464e-02 1.382700565743995857e-01 -2.012898001114737934e-02
4.000000000000000000e+01 1.459605009602895631e-01 -2.247190276782562446e-02 1.457945605500475250e-01 -2.243682861046913946e-02
4.100000000000000000e+01 1.536520122360921503e-01 -2.497186008568041959e-02 1.534774670239254790e-01 -2.493295489429214751e-02
4.200000000000000000e+01 1.614892094816891555e-01 -2.766706276767438855e-02 1.613059129922052304e-01 -2.762403118784728662e-02
4.300000000000000000e+01 1.694579635579972765e-01 -3.056340639252852487e-02 1.692657864747278695e-01 -3.051594422920833605e-02
4.400000000000000000e+01 1.775429759389363926e-01 -3.366588209291965228e-02 1.773418073809650275e-01 -3.361367765329370538e-02
4.500000000000000000e+01 1.857278871445890156e-01 -3.697846833652917997e-02 1.855176358053481078e-01 -3.692120393207964923e-02
4.600000000000000000e+01 1.939954112465833713e-01 -4.050403597071061679e-02 1.937760063635206864e-01 -4.044138955797560442e-02
4.700000000000000000e+01 2.023274939082004842e-01 -4.424427004677777830e-02 2.020988860369883344e-01 -4.417591698183520599e-02
4.800000000000000000e+01 2.107054903339522223e-01 -4.819961144831641509e-02 2.104676519064962448e-01 -4.812522632617766138e-02
4.900000000000000000e+01 2.191103585620426397e-01 -5.236922066417193378e-02 2.188632842112201438e-01 -5.228847920993123788e-02
5.000000000000000000e+01 2.275228628092378635e-01 -5.675096520992223281e-02 2.272665694514352241e-01 -5.666354618725444325e-02
5.100000000000000000e+01 2.359237811262419882e-01 -6.134143126496965914e-02 2.356583077984930608e-01 -6.124701836621643247e-02
5.200000000000000000e+01 2.442936175828763212e-01 -6.613566621450650551e-02 2.440190257506981153e-01 -6.603395038113124560e-02
5.300000000000000000e+01 2.526147982799859526e-01 -7.112840751542359730e-02 2.523311690589603029e-01 -7.101908724312155918e-02
5.400000000000000000e+01 2.608688295653583955e-01 -7.631240648212517241e-02 2.605762650243889644e-01 -7.619519089359516606e-02
5.500000000000000000e+01 2.690385072069091388e-01 -8.167969163020916135e-02 2.687371286089861866e-01 -8.155430149202791412e-02
5.600000000000000000e+01 2.771075502251191258e-01 -8.722138744984686554e-02 2.767974968218402942e-01 -8.708755650392202563e-02
5.700000000000000000e+01 2.850602446917522848e-01 -9.292747532691975065e-02 2.847416732246202398e-01 -9.278495207663145505e-02
5.800000000000000000e+01 2.928834925868490369e-01 -9.878835868343749382e-02 2.925565733060017659e-01 -9.863690547444625700e-02
5.900000000000000000e+01 3.005639309749566501e-01 -1.047928347511858926e-01 3.002288486484894214e-01 -1.046322304279581616e-01
6.000000000000000000e+01 3.080899772605269482e-01 -1.109296642985870274e-01 3.077469287558215472e-01 -1.107597041663329618e-01];
end %% UMNAST DATA WO skin
if 1
UM_NAST_W_skin=[0.000000000000000000e+00 0.000000000000000000e+00 0.000000000000000000e+00 0.000000000000000000e+00 0.000000000000000000e+00
1.000000000000000000e+00 6.899771573056378193e-05 -4.954936683176924817e-09 6.905797004457201187e-05 -4.941647535616766618e-09
2.000000000000000000e+00 2.761074527100788878e-04 -7.869655482828363802e-08 2.763485490865794179e-04 -7.871221785471504973e-08
3.000000000000000000e+00 6.216782889344816664e-04 -3.983534344609296340e-07 6.222211106066784974e-04 -3.986473329220530104e-07
4.000000000000000000e+00 1.106292471988010563e-03 -1.260803740188443101e-06 1.107258370649036924e-03 -1.261972133792532702e-06
5.000000000000000000e+00 1.730765170715292591e-03 -3.085180082851302075e-06 1.732276152838335996e-03 -3.088308999865674309e-06
6.000000000000000000e+00 2.496144994672086070e-03 -6.416396950870151272e-06 2.498323912872557704e-03 -6.423209018890929656e-06
7.000000000000000000e+00 3.403713591324048805e-03 -1.192971466690284643e-05 3.406684337092190634e-03 -1.194272121396444675e-05
8.000000000000000000e+00 4.454986085470971635e-03 -2.043636957416161692e-05 4.458873774865516719e-03 -2.045902915615016582e-05
9.000000000000000000e+00 5.651710750556458024e-03 -3.289029211817062759e-05 5.656641899246834561e-03 -3.292717659608701553e-05
1.000000000000000000e+01 6.996003912355751482e-03 -5.039789610372658046e-05 7.002106760439830158e-03 -5.045486830623779895e-05
1.100000000000000000e+01 8.489840292040265468e-03 -7.422025378833740916e-05 8.497244637947579463e-03 -7.430464703062078513e-05
1.200000000000000000e+01 1.013576985193237988e-02 -1.057923622245215967e-04 1.014460755585324184e-02 -1.059131825669190619e-04
1.300000000000000000e+01 1.193646355471360103e-02 -1.467290638466067776e-04 1.194686861105523010e-02 -1.468971985230105304e-04
1.400000000000000000e+01 1.389506095214551595e-02 -1.988459052851831999e-04 1.390716987698796189e-02 -1.990743552966467433e-04
1.500000000000000000e+01 1.601423692026188172e-02 -2.641476871252379510e-04 1.602818833414989055e-02 -2.644517864677231600e-04
1.600000000000000000e+01 1.829780320706275026e-02 -3.448889674875221800e-04 1.831373878742159275e-02 -3.452866717992275625e-04
1.700000000000000000e+01 2.074878930986107442e-02 -4.435305056965654913e-04 2.076685309784264549e-02 -4.440426304207489849e-04
1.800000000000000000e+01 2.337116369440595670e-02 -5.628153118077960926e-04 2.339150287634379419e-02 -5.634658579143358992e-04
1.900000000000000000e+01 2.616920853386884085e-02 -7.057740536913215124e-04 2.619197368153670588e-02 -7.065905392711346877e-04
2.000000000000000000e+01 2.914633986023595913e-02 -8.756797498963297954e-04 2.917168416599470737e-02 -8.766934889204991421e-04
2.100000000000000000e+01 3.230750449460707829e-02 -1.076197508722231966e-03 3.233558504013985674e-02 -1.077444062154819804e-03
2.200000000000000000e+01 3.565632648141307814e-02 -1.311242930740030843e-03 3.568730308905394139e-02 -1.312762394088173856e-03
2.300000000000000000e+01 3.919804302067495666e-02 -1.585194294573821772e-03 3.923207957667478735e-02 -1.587031829022533813e-03
2.400000000000000000e+01 4.293678151692657124e-02 -1.902731789283573782e-03 4.297404499877227613e-02 -1.904937967293851564e-03
2.500000000000000000e+01 4.687671340476010085e-02 -2.268930671896707274e-03 4.691737387946757348e-02 -2.271561929458432161e-03
2.600000000000000000e+01 5.102315604501062724e-02 -2.689403485794605864e-03 5.106738758184854038e-02 -2.692522737498204144e-03
2.700000000000000000e+01 5.537975086642935030e-02 -3.170053271587813803e-03 5.542773008475444102e-02 -3.173730241023853260e-03
2.800000000000000000e+01 5.995166109507303609e-02 -3.717424698130078475e-03 6.000356837866661908e-02 -3.721736651185469924e-03
2.900000000000000000e+01 6.474212891645314549e-02 -4.338344059594989588e-03 6.479814675341559471e-02 -4.343376123281283974e-03
3.000000000000000000e+01 6.975587871715313582e-02 -5.040350050565023388e-03 6.981619286564598459e-02 -5.046196025598748136e-03
3.100000000000000000e+01 7.499543955076831692e-02 -5.831230728593816970e-03 7.506023714338021235e-02 -5.837993369312455272e-03
3.200000000000000000e+01 8.046422157681465404e-02 -6.719455360621573448e-03 8.053369177548092006e-02 -6.727247150059012526e-03
3.300000000000000000e+01 8.616519962335034144e-02 -7.714024405642949667e-03 8.623953317282659348e-02 -7.722968157054088678e-03
3.400000000000000000e+01 9.209898548068430613e-02 -8.824110311882349400e-03 9.217837266210233971e-02 -8.834339357155829298e-03
3.500000000000000000e+01 9.826756764524863241e-02 -1.005971910085656784e-02 9.835219932398142628e-02 -1.007137823799808540e-02
3.600000000000000000e+01 1.046697578260112338e-01 -1.143081382735322560e-02 1.047598227226385209e-01 -1.144405926052205480e-02
3.700000000000000000e+01 1.113055358606004352e-01 -1.294815739967491997e-02 1.114012214200449241e-01 -1.296315764725275432e-02
3.800000000000000000e+01 1.181714035149858122e-01 -1.462226626524243400e-02 1.182728929236282617e-01 -1.463920186552247760e-02
3.900000000000000000e+01 1.252641942749966320e-01 -1.646420079468891018e-02 1.253716666378574818e-01 -1.648326492063967308e-02
4.000000000000000000e+01 1.325793715720435528e-01 -1.848513935888285165e-02 1.326930006848367205e-01 -1.850653794473944291e-02
4.100000000000000000e+01 1.401089581281231844e-01 -2.069566917782905691e-02 1.402289095288751508e-01 -2.071962023048334878e-02
4.200000000000000000e+01 1.478451210001839600e-01 -2.310666035973696353e-02 1.479715520143912999e-01 -2.313339427919258728e-02
4.300000000000000000e+01 1.557776997021012022e-01 -2.572845414208113635e-02 1.559107574428585108e-01 -2.575821311046300188e-02
4.400000000000000000e+01 1.638947535871270178e-01 -2.857085215353138974e-02 1.640345734254878285e-01 -2.860388951559666992e-02
4.500000000000000000e+01 1.721832570213941427e-01 -3.164320890997029956e-02 1.723299616663460654e-01 -3.167978866746945510e-02
4.600000000000000000e+01 1.806263433599170076e-01 -3.495320051215011770e-02 1.807800396177100533e-01 -3.499359539565283228e-02
4.700000000000000000e+01 1.892075144472905035e-01 -3.850818637945085943e-02 1.893682935733367600e-01 -3.855267750742108479e-02
4.800000000000000000e+01 1.979080262292448600e-01 -4.231404016011297564e-02 1.980759620890174821e-01 -4.236291534944114368e-02
4.900000000000000000e+01 2.067077181910614014e-01 -4.637524002591542072e-02 2.068828661476832531e-01 -4.642879221450357807e-02
5.000000000000000000e+01 2.155852086929226363e-01 -5.069473624993592331e-02 2.157676046846938867e-01 -5.075326177268374428e-02
5.100000000000000000e+01 2.245181256257285374e-01 -5.527384562945747426e-02 2.247077854628608817e-01 -5.533764237818150633e-02
5.200000000000000000e+01 2.334833661546238948e-01 -6.011217747260727551e-02 2.336802850584748514e-01 -6.018154297568645283e-02
5.300000000000000000e+01 2.424573777514429929e-01 -6.520759458281383258e-02 2.426615301515561429e-01 -6.528282404369184500e-02
5.400000000000000000e+01 2.514157405136544510e-01 -7.055577135634710784e-02 2.516270794279149015e-01 -7.063715516013258089e-02
5.500000000000000000e+01 2.603363304037279446e-01 -7.615197994628830624e-02 2.605547898185897049e-01 -7.623980332374474811e-02
5.600000000000000000e+01 2.691952762437732072e-01 -8.198854783391679169e-02 2.694207696381503703e-01 -8.208308745582426624e-02
5.700000000000000000e+01 2.779701412171773911e-01 -8.805669216319217396e-02 2.782025630678784944e-01 -8.815821493630648931e-02
5.800000000000000000e+01 2.866394426407590235e-01 -9.434622162056632844e-02 2.868786694546650029e-01 -9.445498311589639595e-02
5.900000000000000000e+01 2.951828727671122476e-01 -1.008456909198847118e-01 2.954287642972128203e-01 -1.009619339749621147e-01
6.000000000000000000e+01 3.035808056260105303e-01 -1.075420078955462988e-01 3.038332054554400141e-01 -1.076659606858788032e-01];
end %% UMNAST DATA W skin
if 1
sharpy_WO_skin=[1.000000000000000000e+00 8.040940441869363800e-05
2.000000000000000000e+00 3.217368166836035402e-04
3.000000000000000000e+00 7.242788383867615649e-04
4.000000000000000000e+00 1.288528035633102961e-03
5.000000000000000000e+00 2.015169153008880987e-03
6.000000000000000000e+00 2.905076076883640005e-03
7.000000000000000000e+00 3.959311016182898851e-03
8.000000000000000000e+00 5.179106409542957867e-03
9.000000000000000000e+00 6.565872831983228346e-03
1.000000000000000000e+01 8.128034733739811224e-03
1.100000000000000000e+01 9.856919935125383822e-03
1.200000000000000000e+01 1.176000172744211258e-02
1.300000000000000000e+01 1.383771744344325545e-02
1.400000000000000000e+01 1.609315078501561552e-02
1.500000000000000000e+01 1.852874249817798233e-02
1.600000000000000000e+01 2.114701092661074380e-02
1.700000000000000000e+01 2.395049244236125904e-02
1.800000000000000000e+01 2.694180115667756462e-02
1.900000000000000000e+01 3.012345956757878432e-02
2.000000000000000000e+01 3.349809822830669692e-02
2.100000000000000000e+01 3.706807747077707493e-02
2.200000000000000000e+01 4.083576520394494730e-02
2.300000000000000000e+01 4.487784625126844951e-02
2.400000000000000000e+01 4.906055511379830980e-02
2.500000000000000000e+01 5.344796806109395476e-02
2.600000000000000000e+01 5.804136598635621647e-02
2.700000000000000000e+01 6.284139151870225815e-02
2.800000000000000000e+01 6.784796924856836831e-02
2.900000000000000000e+01 7.306075890408210427e-02
3.000000000000000000e+01 7.847844023724560858e-02
3.100000000000000000e+01 8.409889009794149772e-02
3.200000000000000000e+01 8.994023857037933278e-02
3.300000000000000000e+01 9.595787255215985911e-02
3.400000000000000000e+01 1.021655838546145501e-01
3.500000000000000000e+01 1.085583672389582310e-01
3.600000000000000000e+01 1.151268992479245606e-01
3.700000000000000000e+01 1.218636045034976328e-01
3.800000000000000000e+01 1.287586398101896734e-01
3.900000000000000000e+01 1.358007783429377724e-01
4.000000000000000000e+01 1.429783015858903383e-01
4.100000000000000000e+01 1.502785029130883909e-01
4.200000000000000000e+01 1.576866008209024117e-01
4.300000000000000000e+01 1.651882141146358285e-01
4.400000000000000000e+01 1.727686637138771963e-01
4.500000000000000000e+01 1.804120924009835203e-01
4.600000000000000000e+01 1.881013569137417463e-01
4.700000000000000000e+01 1.958215917275751283e-01
4.800000000000000000e+01 2.035557602689156420e-01
4.900000000000000000e+01 2.112892916084291028e-01
5.000000000000000000e+01 2.190060590383147432e-01
5.100000000000000000e+01 2.266902133843062273e-01
5.200000000000000000e+01 2.343298494548349820e-01
5.300000000000000000e+01 2.419077823772721458e-01
5.400000000000000000e+01 2.494131955922129773e-01
5.500000000000000000e+01 2.568362626490177103e-01
5.600000000000000000e+01 2.641637315676447217e-01
5.700000000000000000e+01 2.713814024260809421e-01
5.800000000000000000e+01 2.784824027694886017e-01
5.900000000000000000e+01 2.854492381930368028e-01
6.000000000000000000e+01 2.922961027849404481e-01];    
end %% Sharpy WO skin
if 1
sharpy_W_skin=[1.000000000000000000e+00 7.155397993338608823e-05
2.000000000000000000e+00 2.863270795808943491e-04
3.000000000000000000e+00 6.446528730082219270e-04
4.000000000000000000e+00 1.147247273734484842e-03
5.000000000000000000e+00 1.794830643252610328e-03
6.000000000000000000e+00 2.588483827189974433e-03
7.000000000000000000e+00 3.529520267727781317e-03
8.000000000000000000e+00 4.619477018695018061e-03
9.000000000000000000e+00 5.860111706132495671e-03
1.000000000000000000e+01 7.253409395733322572e-03
1.100000000000000000e+01 8.801576575302954772e-03
1.200000000000000000e+01 1.050702616295359944e-02
1.300000000000000000e+01 1.237237245553070991e-02
1.400000000000000000e+01 1.440043796212259718e-02
1.500000000000000000e+01 1.659422557328252626e-02
1.600000000000000000e+01 1.895690447026976769e-02
1.700000000000000000e+01 2.149178030710760176e-02
1.800000000000000000e+01 2.420233478812264596e-02
1.900000000000000000e+01 2.709213623885837335e-02
2.000000000000000000e+01 3.016483952076654332e-02
2.100000000000000000e+01 3.342416613884860443e-02
2.200000000000000000e+01 3.687386442890851906e-02
2.300000000000000000e+01 4.061535078427001150e-02
2.400000000000000000e+01 4.447647303608825986e-02
2.500000000000000000e+01 4.854171890906801290e-02
2.600000000000000000e+01 5.281434800805680924e-02
2.700000000000000000e+01 5.729781510791241012e-02
2.800000000000000000e+01 6.199492762265899903e-02
2.900000000000000000e+01 6.690813366323578038e-02
3.000000000000000000e+01 7.207479391248673706e-02
3.100000000000000000e+01 7.743102502528081965e-02
3.200000000000000000e+01 8.300725919517536189e-02
3.300000000000000000e+01 8.880296323857432561e-02
3.400000000000000000e+01 9.481684974648894870e-02
3.500000000000000000e+01 1.010456511655224432e-01
3.600000000000000000e+01 1.074858512817019746e-01
3.700000000000000000e+01 1.141317871365144371e-01
3.800000000000000000e+01 1.209768561552619637e-01
3.900000000000000000e+01 1.280128744897133797e-01
4.000000000000000000e+01 1.352296820957962775e-01
4.100000000000000000e+01 1.426160338314854115e-01
4.200000000000000000e+01 1.501597002957190674e-01
4.300000000000000000e+01 1.578453899405561911e-01
4.400000000000000000e+01 1.656578167021760806e-01
4.500000000000000000e+01 1.735808115841157850e-01
4.600000000000000000e+01 1.815968262623248730e-01
4.700000000000000000e+01 1.896867378664073844e-01
4.800000000000000000e+01 1.978310357695769184e-01
4.900000000000000000e+01 2.060117935190705352e-01
5.000000000000000000e+01 2.142089217783802180e-01
5.100000000000000000e+01 2.224046029770364030e-01
5.200000000000000000e+01 2.305789490907561579e-01
5.300000000000000000e+01 2.387160243650698066e-01
5.400000000000000000e+01 2.467973417960250826e-01
5.500000000000000000e+01 2.548055488347066300e-01
5.600000000000000000e+01 2.627260680927051006e-01
5.700000000000000000e+01 2.705482033486273363e-01
5.800000000000000000e+01 2.782536437526919593e-01
5.900000000000000000e+01 2.858372344550859645e-01
6.000000000000000000e+01 2.932785716752857041e-01];    
end %% Sharpy W skin


figure (2)
plot(0.5*1.225*UM_NAST_W_skin(1:10:end,1).^2,UM_NAST_W_skin(1:10:end,2)/0.55*100,'c-s',0.5*1.225*UM_NAST_WO_skin(1:10:end,1).^2,UM_NAST_WO_skin(1:10:end,2)/0.55*100,'c:s','LineWidth',2)
plot(0.5*1.225*sharpy_W_skin([1,10:10:end],1).^2,sharpy_W_skin([1,10:10:end],2)/0.55*100,'g-+',0.5*1.225*sharpy_WO_skin([1,10:10:end],1).^2,sharpy_WO_skin([1,10:10:end],2)/0.55*100,'g:+','LineWidth',2)
legend(leg([1:6,9:end]),'location','EastOutside')   

from  database import database


class getSQLDATA():
    def getProfileData(self,queryData):
        #workingProxy=str(str(workingProxy).strip('[').strip(']')) # will add later
        self.query=f'''select * from profile where profileID='{queryData}' and Email in ('AudreyCornishrq3@yahoo.com','AustintgwCameronp@yahoo.com','avahudsonpcz@yahoo.com','AvaNashXn8@yahoo.com','bellahughesjd9@yahoo.com','BellaPaigeM3D@yahoo.com','bellasimpsonjgp@yahoo.com','BenjaminzbVAveryq@yahoo.com','BernadetteHarrisfrj@yahoo.com','BlakelMaHowardj@yahoo.com','blakewtwrutherfordx@yahoo.com','Boris17jThomsoni@yahoo.com','BorisAsIClarkn@yahoo.com','BorisklCMcGrathy@yahoo.com','Brandon5qlOlivert@yahoo.com','BrandonlDLBallp@yahoo.com','BrandonrIXButlerg@yahoo.com','BrandonuBkWilsong@yahoo.com','BrandonZRYJamesm@yahoo.com','Briandg6Carrx@yahoo.com','Cameron2R2Jamesf@yahoo.com','CameronAr0Clarksonw@yahoo.com','CameronP0wSharpx@yahoo.com','CarliP0Vaughanz@yahoo.com','CarluxzGibsonh@yahoo.com','carolineturnersz1@yahoo.com','CarolLeeEPZ@yahoo.com','CarolStewartQsw@yahoo.com','CarolynHarrispmQ@yahoo.com','CarolynReidbt1@yahoo.com','carolynwelchknw@yahoo.com','CharleseFmChapmany@yahoo.com','CharlesRdSParri@yahoo.com','CharlesuAxHodgesj@yahoo.com','Colin1GBWalshm@yahoo.com','ColinMVDMaye@yahoo.com','Connor9O8Poolea@yahoo.com','ConnorLCnChurchillk@yahoo.com','DanpLOPaigez@yahoo.com','DanwHqRossg@yahoo.com','DavidkFcMartink@yahoo.com','DavidvzbFergusony@yahoo.com','DominicLhqMcGratha@yahoo.com','DominicM40Rossr@yahoo.com','Dominics8NFraserw@yahoo.com','DominicuPMMackayl@yahoo.com','DominicVZmMackayo@yahoo.com','DonnaLambertnUI@yahoo.com','donnarossaws@yahoo.com','dorothysharpj5o@yahoo.com','Dylan5HTParru@yahoo.com','EmilyAllanbmA@yahoo.com','ErickkiDaviesx@yahoo.com','EvaniKqKerrp@yahoo.com','Evanr47Walshg@yahoo.com','faithcornishmbj@yahoo.com','FaithMathisIkq@yahoo.com','faithmorrisonwvm@yahoo.com','FelicityHillhYL@yahoo.com','FelicityMarshall19a@yahoo.com','felicityrandalldxy@yahoo.com','FelicityVanceuye@yahoo.com','FionaBucklandqgm@yahoo.com','FionaDuncantZc@yahoo.com','FionaHardacreUNl@yahoo.com','FionaOgden0r6@yahoo.com','FionaPaynepm9@yahoo.com','fionaquinnvxc@yahoo.com','Frank1jRKellyu@yahoo.com','Frank9BaLawrencer@yahoo.com','Gavind66Gibsonk@yahoo.com','GavinD9vPiperp@yahoo.com','GavinIyjBerryb@yahoo.com','GavinR7RCornishz@yahoo.com','GordonDoBHarrisz@yahoo.com','GordonRyOEllisony@yahoo.com','gracetaylor3mq@yahoo.com','Harryd5tJohnstong@yahoo.com','HarryksoCampbellj@yahoo.com','Harryr6WEllisonv@yahoo.com','HeatherCarrdJj@yahoo.com','heathergilldfe@yahoo.com','HeatherOliverdIp@yahoo.com','HeatherWrightPql@yahoo.com','IanEd3Hillb@yahoo.com','IanH82Abrahamt@yahoo.com','IanPV5Arnoldw@yahoo.com','IanWL6Jacksonp@yahoo.com','irenepayneier@yahoo.com','IreneSkinnerjY4@yahoo.com','IsaaczZeButlerw@yahoo.com','JackdXpVancem@yahoo.com','Jackg1mJamesm@yahoo.com','Jackhw2Gloverh@yahoo.com','Jacob03FWatsonm@yahoo.com','JacobeHSSimpsons@yahoo.com','JacobyKWPeakeh@yahoo.com','JakenKIMitchellp@yahoo.com','JakewthLawrenced@yahoo.com','James7VkNolane@yahoo.com','JamesOvnBurgessi@yahoo.com','JamesTAgClarksona@yahoo.com','JanWelchcA7@yahoo.com','JasmineLangdonAYg@yahoo.com','Jasonl4yLymanl@yahoo.com','JasonVAQWhiteg@yahoo.com','JasonWbcDowdw@yahoo.com','JasonWDiRobertsg@yahoo.com','JenniferClarksonGmo@yahoo.com','jenniferkerryyy@yahoo.com','JenniferWilkinsdvk@yahoo.com','joanhamiltonj7q@yahoo.com','joannenashmvj@yahoo.com','JoeDfpTuckerp@yahoo.com','Joep82Averyr@yahoo.com','John9RIYoungd@yahoo.com','JohnH4yTuckerw@yahoo.com','Jonathann9HRussello@yahoo.com','Jonathanuq6Ellisony@yahoo.com','JonathanyLHBakeru@yahoo.com','JosephV02Scotte@yahoo.com','JoshuaNN1Thomsonu@yahoo.com','JuliaMorrisonB7I@yahoo.com','Julianh8kLambertd@yahoo.com','JulianQBUVancep@yahoo.com','JuliaScottwRr@yahoo.com','KatherineBlakepPe@yahoo.com','KatherineHendersond82@yahoo.com.jso','Keith9aaFishera@yahoo.com','KeithcsDFraserr@yahoo.com','KeithhDeSpringert@yahoo.com','KevinRjyClarksonf@yahoo.com','KevintzpMackayh@yahoo.com','KevinydnKellyn@yahoo.com','KylieScotte6L@yahoo.com','kyliesimpsonqq5@yahoo.com','LeahMorganRKx@yahoo.com','LeonarddZGWilkinsr@yahoo.com','LeonardHoFWatsonu@yahoo.com','Leonardz3RFraserv@yahoo.com','LiamNPLRobertsonu@yahoo.com','LillianBurgessH8s@yahoo.com','lilypaigehsh@yahoo.com','LucasegNParsonsx@yahoo.com','LucasFNVGloverq@yahoo.com','LucaspEaPooleb@yahoo.com','LucasQNVJacksonm@yahoo.com','LukeJ1vCampbellc@yahoo.com','LukeRRkWatsonm@yahoo.com','MariaForsythcpf@yahoo.com','maryhunter5iy@yahoo.com','MattaFVTuckere@yahoo.com','MaxBqeMurrayp@yahoo.com','MaxCJAGlovert@yahoo.com','MaxmOKKingt@yahoo.com','MeganColemanNoE@yahoo.com','melaniedavidsoni3r@yahoo.com','Michael3GKRamplingw@yahoo.com','MichaelqeTRossm@yahoo.com','MichelleLymanUVP@yahoo.com','MollyPullmangal@yahoo.com','NatalieBlackepd@yahoo.com','NathanAPSWelchg@yahoo.com','NathanLaJRosss@yahoo.com','NeileluEllisonn@yahoo.com','Oliver0VORobertsp@yahoo.com','OliverpRBForsythd@yahoo.com','OliverTOnRobertst@yahoo.com','OliverXxNWilsonv@yahoo.com','Owen1WQCarrn@yahoo.com','OwenehBNorthq@yahoo.com','PaulbowGrantx@yahoo.com','PaulouTPeakeb@yahoo.com','PenelopeWilkinsHUk@yahoo.com','PetervRAHillu@yahoo.com','Peterwa9Wilsonk@yahoo.com','PippaPowell0QN@yahoo.com','rebeccafisherixh@yahoo.com','Richardv0jEllisonz@yahoo.com','robertiqupooleh@yahoo.com','Robertjd8Butlern@yahoo.com','RobertjoSMitchellm@yahoo.com','RobertLipAlsoph@yahoo.com','ruthfergusonnku@yahoo.com','Sam8gcLewish@yahoo.com','SamanthaJohnstonC3n@yahoo.com','SamCIOWalshr@yahoo.com','SamexYOlivery@yahoo.com','SamtXVWhitex@yahoo.com','sarahhenderson6lv@yahoo.com','sarahrobertsn1s@yahoo.com','Seana4lHodgesh@yahoo.com','SeanLlKSkinnerk@yahoo.com','SeanwoNLambertj@yahoo.com','Simon9RLJonesb@yahoo.com','SimonpskNolanj@yahoo.com','SophieAbrahamQFb@yahoo.com','sophieballgei@yahoo.com','SophieClarksonP8W@yahoo.com','SophieEdmundspio@yahoo.com','SophiePeakeOVc@yahoo.com','stephaniemackayomf@yahoo.com','StephanieMorrisongCk@yahoo.com','Stephen4VvNewmanl@yahoo.com','Stevenjt9Murrayt@yahoo.com','Stevent5YKerrj@yahoo.com','StewartklBVancef@yahoo.com','StewartOU8Skinnerw@yahoo.com','StewartSRMHardacreg@yahoo.com','StewartYRdMcDonaldm@yahoo.com','suewhitemrw@yahoo.com','Thomas0SJStewarty@yahoo.com','Thomas0VKBakerw@yahoo.com','ThomasgBHHarrism@yahoo.com','ThomasSSLColemane@yahoo.com','TimANRMillerc@yahoo.com','TimY3MSimpsond@yahoo.com','TrevordrPWilkinsx@yahoo.com','TrevorMoyPeterse@yahoo.com','UnaJacksonIMy@yahoo.com','unarobertsonumw@yahoo.com','victoriaallanteo@yahoo.com','wandafraserizd@yahoo.com','WarrenSstIncel@yahoo.com','WendyParsons38x@yahoo.com','WilliamQDcPaigea@yahoo.com','williamt0hmorganh@yahoo.com','yvonnebaileycah@yahoo.com','ZoeFraser3cx@yahoo.com','ZoeSutherlandTfx@yahoo.com');'''
        #self.query=f'''select * from profile where profileID='{queryData}' and Proxy_IP in '{workingProxy}' limit 1;''' # will add later
        self.output=database.db(self.query)
        return(self.output)
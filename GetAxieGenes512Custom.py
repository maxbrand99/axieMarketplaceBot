import json


def getAxieGeneImage512(axie_genes):
    def getPartsFromGroup(part, group):
        dClass = classGeneMap[group[25:30]]
        dBin = group[30:38]

        r1Class = classGeneMap[group[38:43]]
        r1Bin = group[43:51]

        r2Class = classGeneMap[group[51:56]]
        r2Bin = group[56:64]

        try:
            return {
                "d": binarytraits[dClass][part][dBin][group[21:25]],
                "r1": binarytraits[r1Class][part][r1Bin]["0000"],
                "r2": binarytraits[r2Class][part][r2Bin]["0000"]
            }
        except:
            if group[21:25] == "0101" or group[21:25] == "0010":
                return {
                    "d": binarytraits[dClass][part][dBin]["0000"],
                    "r1": binarytraits[r1Class][part][r1Bin]["0000"],
                    "r2": binarytraits[r2Class][part][r2Bin]["0000"]
                }
            print(part)
            print(group)
            print(dClass)
            print(dBin)
            print(group[21:25])
            raise "success = false"

    binarytraits = {
        "beast": {
            "eyes": {
                "00001000": {
                    "0000": {"partId":"ears-puppy", "class":"beast", "specialGenes":None,"type":"ears", "name":"Puppy"}
                },
                "00000010": {
                    "0000": {"partId":"eyes-zeal", "class":"beast", "specialGenes":None,"type":"eyes", "name":"Zeal"},
                    "0001": {"partId":"eyes-calico-zeal", "class":"beast", "specialGenes":"mystic", "type":"eyes", "name":"Calico Zeal"}
                },
                "00000100": {
                    "0000": {"partId":"eyes-little-peas", "class":"beast", "specialGenes":None,"type":"eyes", "name":"Little Peas"},
                    "0100": {"partId":"eyes-snowflakes", "class":"beast", "specialGenes":"xmas", "type":"eyes", "name":"Snowflakes"}
                },
                "00001010": {
                    "0000": {"partId":"eyes-chubby", "class":"beast", "specialGenes":None,"type":"eyes", "name":"Chubby"}
                }
            },
            "ears": {
                "00001010": {
                    "0000": {"partId":"ears-puppy", "class":"beast", "specialGenes":None,"type":"ears", "name":"Puppy"}
                },
                "00000100": {
                    "0000": {"partId":"mouth-nut-cracker", "class":"beast", "specialGenes":None,"type":"mouth", "name":"Nut Cracker"}
                },
                "00000010": {
                    "0000": {"partId":"ears-nyan", "class":"beast", "specialGenes":None,"type":"ears", "name":"Nyan"},
                    "0001": {"partId":"ears-pointy-nyan", "class":"beast", "specialGenes":"mystic", "type":"ears", "name":"Pointy Nyan"},
                    "0110": {"partId":"ears-coca", "class":"beast", "name":"Coca", "specialGenes":"summer", "type":"ears"},
                    "1001": {"partId":"ears-coca-shiny", "class":"beast", "name":"Coca Shiny", "specialGenes":"shiny", "type":"ears"}
                },
                "00000110": {
                    "0000": {"partId":"ears-innocent-lamb", "class":"beast", "specialGenes":None,"type":"ears", "name":"Innocent Lamb"},
                    "0100": {"partId":"ears-merry-lamb", "class":"beast", "specialGenes":"xmas", "type":"ears", "name":"Merry Lamb"}
                },
                "00001000": {
                    "0000": {"partId":"ears-zen", "class":"beast", "specialGenes":None,"type":"ears", "name":"Zen"}
                },
                "00001100": {
                    "0000": {"partId":"ears-belieber", "class":"beast", "specialGenes":None,"type":"ears", "name":"Belieber"}
                }
            },
            "back": {
                "00001000": {
                    "0011": {"partId":"back-hamaya", "class":"beast", "specialGenes":"japan", "type":"back", "name":"Hamaya"},
                    "0000": {"partId":"back-risky-beast", "class":"beast", "specialGenes":None,"type":"back", "name":"Risky Beast"}
                },
                "00000100": {
                    "0000": {"partId":"back-hero", "class":"beast", "specialGenes":None,"type":"back", "name":"Hero"}
                },
                "00000110": {
                    "0000": {"partId":"back-jaguar", "class":"beast", "specialGenes":None,"type":"back", "name":"Jaguar"}
                },
                "00000010": {
                    "0001": {"partId":"back-hasagi", "class":"beast", "specialGenes":"mystic", "type":"back", "name":"Hasagi"},
                    "0000": {"partId":"back-ronin", "class":"beast", "specialGenes":None,"type":"back", "name":"Ronin"}
                },
                "00001010": {
                    "0000": {"partId":"back-timber", "class":"beast", "specialGenes":None,"type":"back", "name":"Timber"}
                },
                "00001100": {
                    "0000": {"partId":"back-furball", "class":"beast", "specialGenes":None,"type":"back", "name":"Furball"},
                    "0110": {"partId":"back-beach-ball", "class":"beast", "name":"Beach Ball", "specialGenes":"summer", "type":"back"},
                    "1001": {"partId":"back-beach-ball-shiny", "class":"beast", "name":"Beach Ball Shiny", "specialGenes":"shiny", "type":"back"}
                }
            },
            "horn": {
                "00001000": {
                    "0011": {"partId":"horn-umaibo", "class":"beast", "specialGenes":"japan", "type":"horn", "name":"Umaibo"},
                    "0000": {"partId":"horn-pocky", "class":"beast", "specialGenes":None,"type":"horn", "name":"Pocky"}
                },
                "00000100": {
                    "0000": {"partId":"horn-imp", "class":"beast", "specialGenes":None,"type":"horn", "name":"Imp"},
                    "0011": {"partId":"horn-kendama", "class":"beast", "specialGenes":"japan", "type":"horn", "name":"Kendama"}
                },
                "00000110": {
                    "0000": {"partId":"horn-merry", "class":"beast", "specialGenes":None,"type":"horn", "name":"Merry"}
                },
                "00000010": {
                    "0001": {"partId":"horn-winter-branch", "class":"beast", "specialGenes":"mystic", "type":"horn", "name":"Winter Branch"},
                    "0000": {"partId":"horn-little-branch", "class":"beast", "specialGenes":None,"type":"horn", "name":"Little Branch"}
                },
                "00001010": {
                    "0000": {"partId":"horn-dual-blade", "class":"beast", "specialGenes":None,"type":"horn", "name":"Dual Blade"}
                },
                "00001100": {
                    "0000": {"partId":"horn-arco", "class":"beast", "specialGenes":None,"type":"horn", "name":"Arco"}
                }
            },
            "tail": {
                "00000100": {
                    "0000": {"partId":"tail-rice", "class":"beast", "specialGenes":None,"type":"tail", "name":"Rice"}
                },
                "00000010": {
                    "0000": {"partId":"tail-cottontail", "class":"beast", "specialGenes":None,"type":"tail", "name":"Cottontail"},
                    "0001": {"partId":"tail-sakura-cottontail", "class":"beast", "specialGenes":"mystic", "type":"tail", "name":"Sakura Cottontail"},
                    "0110": {"partId":"tail-cotton-candy", "class":"beast", "name":"Cotton Candy", "specialGenes":"summer", "type":"tail"},
                    "1001": {"partId":"tail-cotton-candy-shiny", "class":"beast", "name":"Cotton Candy Shiny", "specialGenes":"shiny", "type":"tail"}
                },
                "00000110": {
                    "0000": {"partId":"tail-shiba", "class":"beast", "specialGenes":None,"type":"tail", "name":"Shiba"}
                },
                "00001000": {
                    "0000": {"partId":"tail-hare", "class":"beast", "specialGenes":None,"type":"tail", "name":"Hare"}
                },
                "00001010": {
                    "0000": {"partId":"mouth-nut-cracker", "class":"beast", "specialGenes":None,"type":"mouth", "name":"Nut Cracker"}
                },
                "00001100": {
                    "0000": {"partId":"tail-gerbil", "class":"beast", "specialGenes":None,"type":"tail", "name":"Gerbil"}
                }
            },
            "mouth": {
                "00000100": {
                    "0000": {"partId":"mouth-goda", "class":"beast", "specialGenes":None,"type":"mouth", "name":"Goda"}
                },
                "00000010": {
                    "0000": {"partId":"mouth-nut-cracker", "class":"beast", "specialGenes":None,"type":"mouth", "name":"Nut Cracker"},
                    "0001": {"partId":"mouth-skull-cracker", "class":"beast", "specialGenes":"mystic", "type":"mouth", "name":"Skull Cracker"}
                },
                "00001000": {
                    "0000": {"partId":"mouth-axie-kiss", "class":"beast", "specialGenes":None,"type":"mouth", "name":"Axie Kiss"}
                },
                "00001010": {
                    "0000": {"partId":"mouth-confident", "class":"beast", "specialGenes":None,"type":"mouth", "name":"Confident"}
                }
            }
        },
        "bug": {
            "mouth": {
                "00001000": {
                    "0011": {"partId":"mouth-kawaii", "class":"bug", "specialGenes":"japan", "type":"mouth", "name":"Kawaii"},
                    "0000": {"partId":"mouth-cute-bunny", "class":"bug", "specialGenes":None,"type":"mouth", "name":"Cute Bunny"}
                },
                "00000010": {
                    "0000": {"partId":"mouth-mosquito", "class":"bug", "specialGenes":None,"type":"mouth", "name":"Mosquito"},
                    "0001": {"partId":"mouth-feasting-mosquito", "class":"bug", "specialGenes":"mystic", "type":"mouth", "name":"Feasting Mosquito"}
                },
                "00000100": {
                    "0000": {"partId":"mouth-pincer", "class":"bug", "specialGenes":None,"type":"mouth", "name":"Pincer"}
                },
                "00001010": {
                    "0000": {"partId":"mouth-square-teeth", "class":"bug", "specialGenes":None,"type":"mouth", "name":"Square Teeth"}
                }
            },
            "horn": {
                "00001010": {
                    "0000": {"partId":"horn-parasite", "class":"bug", "specialGenes":None,"type":"horn", "name":"Parasite"}
                },
                "00000010": {
                    "0000": {"partId":"horn-lagging", "class":"bug", "specialGenes":None,"type":"horn", "name":"Lagging"},
                    "0001": {"partId":"horn-laggingggggg", "class":"bug", "specialGenes":"mystic", "type":"horn", "name":"Laggingggggg"}
                },
                "00000110": {
                    "0000": {"partId":"horn-caterpillars", "class":"bug", "specialGenes":None,"type":"horn", "name":"Caterpillars"}
                },
                "00000100": {
                    "0000": {"partId":"horn-antenna", "class":"bug", "specialGenes":None,"type":"horn", "name":"Antenna"}
                },
                "00001000": {
                    "0000": {"partId":"horn-pliers", "class":"bug", "specialGenes":None,"type":"horn", "name":"Pliers"}
                },
                "00001100": {
                    "0000": {"partId":"horn-leaf-bug", "class":"bug", "specialGenes":None,"type":"horn", "name":"Leaf Bug"}
                }
            },
            "tail": {
                "00001000": {
                    "0000": {"partId":"tail-gravel-ant", "class":"bug", "specialGenes":None,"type":"tail", "name":"Gravel Ant"}
                },
                "00000010": {
                    "0001": {"partId":"tail-fire-ant", "class":"bug", "specialGenes":"mystic", "type":"tail", "name":"Fire Ant"},
                    "0000": {"partId":"tail-ant", "class":"bug", "specialGenes":None,"type":"tail", "name":"Ant"}
                },
                "00000100": {
                    "0000": {"partId":"tail-twin-tail", "class":"bug", "specialGenes":None,"type":"tail", "name":"Twin Tail"}
                },
                "00000110": {
                    "0000": {"partId":"tail-fish-snack", "class":"bug", "specialGenes":None,"type":"tail", "name":"Fish Snack"},
                    "0011": {"partId":"tail-maki", "class":"bug", "specialGenes":"japan", "type":"tail", "name":"Maki"}
                },
                "00001010": {
                    "0000": {"partId":"tail-pupae", "class":"bug", "specialGenes":None,"type":"tail", "name":"Pupae"}
                },
                "00001100": {
                    "0000": {"partId":"tail-thorny-caterpillar", "class":"bug", "specialGenes":None,"type":"tail", "name":"Thorny Caterpillar"}
                }
            },
            "back": {
                "00001000": {
                    "0000": {"partId":"back-sandal", "class":"bug", "specialGenes":None,"type":"back", "name":"Sandal"}
                },
                "00000010": {
                    "0000": {"partId":"back-snail-shell", "class":"bug", "specialGenes":None,"type":"back", "name":"Snail Shell"},
                    "0001": {"partId":"back-starry-shell", "class":"bug", "specialGenes":"mystic", "type":"back", "name":"Starry Shell"}
                },
                "00000100": {
                    "0000": {"partId":"back-garish-worm", "class":"bug", "specialGenes":None,"type":"back", "name":"Garish Worm"},
                    "0100": {"partId":"back-candy-canes", "class":"bug", "specialGenes":"xmas", "type":"back", "name":"Candy Canes"}
                },
                "00000110": {
                    "0000": {"partId":"back-buzz-buzz", "class":"bug", "specialGenes":None,"type":"back", "name":"Buzz Buzz"}
                },
                "00001010": {
                    "0000": {"partId":"back-scarab", "class":"bug", "specialGenes":None,"type":"back", "name":"Scarab"}
                },
                "00001100": {
                    "0000": {"partId":"back-spiky-wing", "class":"bug", "specialGenes":None,"type":"back", "name":"Spiky Wing"}
                }
            },
            "ears": {
                "00000010": {
                    "0000": {"partId":"ears-larva", "class":"bug", "specialGenes":None,"type":"ears", "name":"Larva"},
                    "0001": {"partId":"ears-vector", "class":"bug", "specialGenes":"mystic", "type":"ears", "name":"Vector"}
                },
                "00000110": {
                    "0000": {"partId":"ears-ear-breathing", "class":"bug", "specialGenes":None,"type":"ears", "name":"Ear Breathing"}
                },
                "00000100": {
                    "0000": {"partId":"ears-beetle-spike", "class":"bug", "specialGenes":None,"type":"ears", "name":"Beetle Spike"}
                },
                "00001000": {
                    "0000": {"partId":"horn-leaf-bug", "class":"bug", "specialGenes":None,"type":"horn", "name":"Leaf Bug"}
                },
                "00001010": {
                    "0000": {"partId":"ears-tassels", "class":"bug", "specialGenes":None,"type":"ears", "name":"Tassels"}
                },
                "00001100": {
                    "0011": {"partId":"ears-mon", "class":"bug", "specialGenes":"japan", "type":"ears", "name":"Mon"},
                    "0000": {"partId":"ears-earwing", "class":"bug", "specialGenes":None,"type":"ears", "name":"Earwing"}
                }
            },
            "eyes": {
                "00000010": {
                    "0000": {"partId":"eyes-bookworm", "class":"bug", "specialGenes":None,"type":"eyes", "name":"Bookworm"},
                    "0001": {"partId":"eyes-broken-bookworm", "class":"bug", "specialGenes":"mystic", "type":"eyes", "name":"Broken Bookworm"}
                },
                "00000100": {
                    "0000": {"partId":"eyes-neo", "class":"bug", "specialGenes":None,"type":"eyes", "name":"Neo"},
                    "0110": {"partId":"eyes-flower-sunglasses", "class":"bug", "name":"Flower Sunglasses", "specialGenes":"summer", "type":"eyes"},
                    "1001": {"partId":"eyes-flower-sunglasses-shiny", "class":"bug", "name":"Flower Sunglasses Shiny", "specialGenes":"shiny", "type":"eyes"}
                },
                "00001010": {
                    "0000": {"partId":"eyes-kotaro", "class":"bug", "specialGenes":None,"type":"eyes", "name":"Kotaro?"}
                },
                "00001000": {
                    "0000": {"partId":"eyes-nerdy", "class":"bug", "specialGenes":None,"type":"eyes", "name":"Nerdy"}
                }
            }
        },
        "aquatic": {
            "eyes": {
                "00001000": {
                    "0000": {"partId":"eyes-gero", "class":"aquatic", "specialGenes":None,"type":"eyes", "name":"Gero"}
                },
                "00000010": {
                    "0000": {"partId":"eyes-sleepless", "class":"aquatic", "specialGenes":None,"type":"eyes", "name":"Sleepless"},
                    "0001": {"partId":"eyes-insomnia", "class":"aquatic", "specialGenes":"mystic", "type":"eyes", "name":"Insomnia"},
                    "0011": {"partId":"eyes-yen", "class":"aquatic", "specialGenes":"japan", "type":"eyes", "name":"Yen"}
                },
                "00000100": {
                    "0000": {"partId":"eyes-clear", "class":"aquatic", "specialGenes":None,"type":"eyes", "name":"Clear"}
                },
                "00001010": {
                    "0000": {"partId":"eyes-telescope", "class":"aquatic", "specialGenes":None,"type":"eyes", "name":"Telescope"}
                }
            },
            "mouth": {
                "00001000": {
                    "0000": {"partId":"mouth-risky-fish", "class":"aquatic", "specialGenes":None,"type":"mouth", "name":"Risky Fish"},
                    "0110": {"partId":"mouth-bubble-fish", "class":"aquatic", "name":"Bubble Fish", "specialGenes":"summer", "type":"mouth"},
                    "1001": {"partId":"mouth-bubble-fish-shiny", "class":"aquatic", "name":"Bubble Fish Shiny", "specialGenes":"shiny", "type":"mouth"}
                },
                "00000100": {
                    "0000": {"partId":"mouth-catfish", "class":"aquatic", "specialGenes":None,"type":"mouth", "name":"Catfish"}
                },
                "00000010": {
                    "0000": {"partId":"mouth-lam", "class":"aquatic", "specialGenes":None,"type":"mouth", "name":"Lam"},
                    "0001": {"partId":"mouth-lam-handsome", "class":"aquatic", "specialGenes":"mystic", "type":"mouth", "name":"Lam Handsome"}
                },
                "00001010": {
                    "0000": {"partId":"mouth-piranha", "class":"aquatic", "specialGenes":None,"type":"mouth", "name":"Piranha"},
                    "0011": {"partId":"mouth-geisha", "class":"aquatic", "specialGenes":"japan", "type":"mouth", "name":"Geisha"}
                }
            },
            "horn": {
                "00001100": {
                    "0000": {"partId":"horn-shoal-star", "class":"aquatic", "specialGenes":None,"type":"horn", "name":"Shoal Star"}
                },
                "00000110": {
                    "0000": {"partId":"horn-clamshell", "class":"aquatic", "specialGenes":None,"type":"horn", "name":"Clamshell"}
                },
                "00000010": {
                    "0000": {"partId":"horn-babylonia", "class":"aquatic", "specialGenes":None,"type":"horn", "name":"Babylonia"},
                    "0001": {"partId":"horn-candy-babylonia", "class":"aquatic", "specialGenes":"mystic", "type":"horn", "name":"Candy Babylonia"}
                },
                "00000100": {
                    "0000": {"partId":"horn-teal-shell", "class":"aquatic", "specialGenes":None,"type":"horn", "name":"Teal Shell"}
                },
                "00001000": {
                    "0000": {"partId":"back-anemone", "class":"aquatic", "specialGenes":None,"type":"back", "name":"Anemone"}
                },
                "00001010": {
                    "0000": {"partId":"horn-oranda", "class":"aquatic", "specialGenes":None,"type":"horn", "name":"Oranda"}
                }
            },
            "ears": {
                "00000010": {
                    "0000": {"partId":"tail-nimo", "class":"aquatic", "specialGenes":None,"type":"tail", "name":"Nimo"},
                    "0001": {"partId":"ears-red-nimo", "class":"aquatic", "specialGenes":"mystic", "type":"ears", "name":"Red Nimo"}
                },
                "00000110": {
                    "0000": {"partId":"ears-bubblemaker", "class":"aquatic", "specialGenes":None,"type":"ears", "name":"Bubblemaker"}
                },
                "00000100": {
                    "0000": {"partId":"ears-tiny-fan", "class":"aquatic", "specialGenes":None,"type":"ears", "name":"Tiny Fan"}
                },
                "00001000": {
                    "0000": {"partId":"ears-inkling", "class":"aquatic", "specialGenes":None,"type":"ears", "name":"Inkling"}
                },
                "00001010": {
                    "0000": {"partId":"ears-gill", "class":"aquatic", "specialGenes":None,"type":"ears", "name":"Gill"}
                },
                "00001100": {
                    "0000": {"partId":"ears-seaslug", "class":"aquatic", "specialGenes":None,"type":"ears", "name":"Seaslug"}
                }
            },
            "tail": {
                "00000010": {
                    "0000": {"partId":"tail-koi", "class":"aquatic", "specialGenes":None,"type":"tail", "name":"Koi"},
                    "0001": {"partId":"tail-kuro-koi", "class":"aquatic", "specialGenes":"mystic", "type":"tail", "name":"Kuro Koi"},
                    "0011": {"partId":"tail-koinobori", "class":"aquatic", "specialGenes":"japan", "type":"tail", "name":"Koinobori"}
                },
                "00000110": {
                    "0000": {"partId":"tail-tadpole", "class":"aquatic", "specialGenes":None,"type":"tail", "name":"Tadpole"}
                },
                "00000100": {
                    "0000": {"partId":"tail-nimo", "class":"aquatic", "specialGenes":None,"type":"tail", "name":"Nimo"}
                },
                "00001010": {
                    "0000": {"partId":"tail-navaga", "class":"aquatic", "specialGenes":None,"type":"tail", "name":"Navaga"}
                },
                "00001000": {
                    "0000": {"partId":"tail-ranchu", "class":"aquatic", "specialGenes":None,"type":"tail", "name":"Ranchu"}
                },
                "00001100": {
                    "0000": {"partId":"tail-shrimp", "class":"aquatic", "specialGenes":None,"type":"tail", "name":"Shrimp"}
                }
            },
            "back": {
                "00000010": {
                    "0000": {"partId":"back-hermit", "class":"aquatic", "specialGenes":None,"type":"back", "name":"Hermit"},
                    "0001": {"partId":"back-crystal-hermit", "class":"aquatic", "specialGenes":"mystic", "type":"back", "name":"Crystal Hermit"}
                },
                "00000100": {
                    "0000": {"partId":"back-blue-moon", "class":"aquatic", "specialGenes":None,"type":"back", "name":"Blue Moon"}
                },
                "00000110": {
                    "0000": {"partId":"back-goldfish", "class":"aquatic", "specialGenes":None,"type":"back", "name":"Goldfish"}
                },
                "00001010": {
                    "0000": {"partId":"back-anemone", "class":"aquatic", "specialGenes":None,"type":"back", "name":"Anemone"}
                },
                "00001000": {
                    "0000": {"partId":"back-sponge", "class":"aquatic", "specialGenes":None,"type":"back", "name":"Sponge"}
                },
                "00001100": {
                    "0000": {"partId":"back-perch", "class":"aquatic", "specialGenes":None,"type":"back", "name":"Perch"}
                }
            }
        },
        "bird": {
            "ears": {
                "00001100": {
                    "0011": {"partId":"ears-karimata", "class":"bird", "specialGenes":"japan", "type":"ears", "name":"Karimata"},
                    "0000": {"partId":"ears-risky-bird", "class":"bird", "specialGenes":None,"type":"ears", "name":"Risky Bird"}
                },
                "00000010": {
                    "0000": {"partId":"ears-pink-cheek", "class":"bird", "specialGenes":None,"type":"ears", "name":"Pink Cheek"},
                    "0001": {"partId":"ears-heart-cheek", "class":"bird", "specialGenes":"mystic", "type":"ears", "name":"Heart Cheek"}
                },
                "00000100": {
                    "0000": {"partId":"ears-early-bird", "class":"bird", "specialGenes":None,"type":"ears", "name":"Early Bird"}
                },
                "00000110": {
                    "0000": {"partId":"ears-owl", "class":"bird", "specialGenes":None,"type":"ears", "name":"Owl"}
                },
                "00001010": {
                    "0000": {"partId":"ears-curly", "class":"bird", "specialGenes":None,"type":"ears", "name":"Curly"}
                },
                "00001000": {
                    "0000": {"partId":"mouth-peace-maker", "class":"bird", "specialGenes":None,"type":"mouth", "name":"Peace Maker"}
                }
            },
            "tail": {
                "00001010": {
                    "0011": {"partId":"tail-omatsuri", "class":"bird", "specialGenes":"japan", "type":"tail", "name":"Omatsuri"},
                    "0000": {"partId":"tail-granmas-fan", "class":"bird", "specialGenes":None,"type":"tail", "name":"Granma's Fan"}
                },
                "00000010": {
                    "0000": {"partId":"tail-swallow", "class":"bird", "specialGenes":None,"type":"tail", "name":"Swallow"},
                    "0001": {"partId":"tail-snowy-swallow", "class":"bird", "specialGenes":"mystic", "type":"tail", "name":"Snowy Swallow"}
                },
                "00000100": {
                    "0000": {"partId":"tail-feather-fan", "class":"bird", "specialGenes":None,"type":"tail", "name":"Feather Fan"}
                },
                "00000110": {
                    "0000": {"partId":"tail-the-last-one", "class":"bird", "specialGenes":None,"type":"tail", "name":"The Last One"}
                },
                "00001000": {
                    "0000": {"partId":"tail-cloud", "class":"bird", "specialGenes":None,"type":"tail", "name":"Cloud"}
                },
                "00001100": {
                    "0000": {"partId":"tail-post-fight", "class":"bird", "specialGenes":None,"type":"tail", "name":"Post Fight"}
                }
            },
            "back": {
                "00000010": {
                    "0000": {"partId":"back-balloon", "class":"bird", "specialGenes":None,"type":"back", "name":"Balloon"},
                    "0001": {"partId":"back-starry-balloon", "class":"bird", "specialGenes":"mystic", "type":"back", "name":"Starry Balloon"}
                },
                "00000110": {
                    "0000": {"partId":"back-raven", "class":"bird", "specialGenes":None,"type":"back", "name":"Raven"}
                },
                "00000100": {
                    "0000": {"partId":"back-cupid", "class":"bird", "specialGenes":None,"type":"back", "name":"Cupid"},
                    "0011": {"partId":"back-origami", "class":"bird", "specialGenes":"japan", "type":"back", "name":"Origami"}
                },
                "00001000": {
                    "0000": {"partId":"back-pigeon-post", "class":"bird", "specialGenes":None,"type":"back", "name":"Pigeon Post"}
                },
                "00001010": {
                    "0000": {"partId":"back-kingfisher", "class":"bird", "specialGenes":None,"type":"back", "name":"Kingfisher"}
                },
                "00001100": {
                    "0000": {"partId":"back-tri-feather", "class":"bird", "specialGenes":None,"type":"back", "name":"Tri Feather"}
                }
            },
            "horn": {
                "00000110": {
                    "0000": {"partId":"horn-trump", "class":"bird", "specialGenes":None,"type":"horn", "name":"Trump"}
                },
                "00000010": {
                    "0000": {"partId":"horn-eggshell", "class":"bird", "specialGenes":None,"type":"horn", "name":"Eggshell"},
                    "0001": {"partId":"horn-golden-shell", "class":"bird", "specialGenes":"mystic", "type":"horn", "name":"Golden Shell"}
                },
                "00000100": {
                    "0000": {"partId":"horn-cuckoo", "class":"bird", "specialGenes":None,"type":"horn", "name":"Cuckoo"}
                },
                "00001000": {
                    "0000": {"partId":"horn-kestrel", "class":"bird", "specialGenes":None,"type":"horn", "name":"Kestrel"}
                },
                "00001010": {
                    "0000": {"partId":"horn-wing-horn", "class":"bird", "specialGenes":None,"type":"horn", "name":"Wing Horn"}
                },
                "00001100": {
                    "0000": {"partId":"horn-feather-spear", "class":"bird", "specialGenes":None,"type":"horn", "name":"Feather Spear"},
                    "0100": {"partId":"horn-spruce-spear", "class":"bird", "specialGenes":"xmas", "type":"horn", "name":"Spruce Spear"}
                }
            },
            "mouth": {
                "00000010": {
                    "0000": {"partId":"mouth-doubletalk", "class":"bird", "specialGenes":None,"type":"mouth", "name":"Doubletalk"},
                    "0001": {"partId":"mouth-mr-doubletalk", "class":"bird", "specialGenes":"mystic", "type":"mouth", "name":"Mr. Doubletalk"}
                },
                "00000100": {
                    "0000": {"partId":"mouth-peace-maker", "class":"bird", "specialGenes":None,"type":"mouth", "name":"Peace Maker"}
                },
                "00001000": {
                    "0000": {"partId":"mouth-hungry-bird", "class":"bird", "specialGenes":None,"type":"mouth", "name":"Hungry Bird"}
                },
                "00001010": {
                    "0000": {"partId":"eyes-little-owl", "class":"bird", "specialGenes":None,"type":"eyes", "name":"Little Owl"}
                }
            },
            "eyes": {
                "00000010": {
                    "0000": {"partId":"eyes-mavis", "class":"bird", "specialGenes":None,"type":"eyes", "name":"Mavis"},
                    "0001": {"partId":"eyes-sky-mavis", "class":"bird", "specialGenes":"mystic", "type":"eyes", "name":"Sky Mavis"}
                },
                "00000100": {
                    "0000": {"partId":"eyes-lucas", "class":"bird", "specialGenes":None,"type":"eyes", "name":"Lucas"}
                },
                "00001010": {
                    "0000": {"partId":"eyes-robin", "class":"bird", "specialGenes":None,"type":"eyes", "name":"Robin"}
                },
                "00001000": {
                    "0000": {"partId":"eyes-little-owl", "class":"bird", "specialGenes":None,"type":"eyes", "name":"Little Owl"}
                }
            }
        },
        "reptile": {
            "eyes": {
                "00001010": {
                    "0011": {"partId":"eyes-kabuki", "class":"reptile", "specialGenes":"japan", "type":"eyes", "name":"Kabuki"},
                    "0000": {"partId":"eyes-topaz", "class":"reptile", "specialGenes":None,"type":"eyes", "name":"Topaz"}
                },
                "00000100": {
                    "0000": {"partId":"eyes-tricky", "class":"reptile", "specialGenes":None,"type":"eyes", "name":"Tricky"}
                },
                "00000010": {
                    "0000": {"partId":"eyes-gecko", "class":"reptile", "specialGenes":None,"type":"eyes", "name":"Gecko"},
                    "0001": {"partId":"eyes-crimson-gecko", "class":"reptile", "specialGenes":"mystic", "type":"eyes", "name":"Crimson Gecko"}
                },
                "00001000": {
                    "0000": {"partId":"eyes-scar", "class":"reptile", "specialGenes":None,"type":"eyes", "name":"Scar"},
                    "0011": {"partId":"eyes-dokuganryu", "class":"reptile", "specialGenes":"japan", "type":"eyes", "name":"Dokuganryu"}
                }
            },
            "mouth": {
                "00001000": {
                    "0000": {"partId":"mouth-razor-bite", "class":"reptile", "specialGenes":None,"type":"mouth", "name":"Razor Bite"}
                },
                "00000100": {
                    "0000": {"partId":"mouth-kotaro", "class":"reptile", "specialGenes":None,"type":"mouth", "name":"Kotaro"}
                },
                "00000010": {
                    "0000": {"partId":"mouth-toothless-bite", "class":"reptile", "specialGenes":None,"type":"mouth", "name":"Toothless Bite"},
                    "0001": {"partId":"mouth-venom-bite", "class":"reptile", "specialGenes":"mystic", "type":"mouth", "name":"Venom Bite"}
                },
                "00001010": {
                    "0000": {"partId":"mouth-tiny-turtle", "class":"reptile", "specialGenes":None,"type":"mouth", "name":"Tiny Turtle"},
                    "0011": {"partId":"mouth-dango", "class":"reptile", "specialGenes":"japan", "type":"mouth", "name":"Dango"},
                    "0101": {"partId":"mouth-tiny-carrot", "class":"reptile", "specialGenes":"xmas", "type":"mouth", "name":"Tiny Carrot"}
                }
            },
            "ears": {
                "00001000": {
                    "0000": {"partId":"ears-small-frill", "class":"reptile", "specialGenes":None,"type":"ears", "name":"Small Frill"}
                },
                "00000110": {
                    "0000": {"partId":"ears-curved-spine", "class":"reptile", "specialGenes":None,"type":"ears", "name":"Curved Spine"}
                },
                "00000100": {
                    "0000": {"partId":"ears-friezard", "class":"reptile", "specialGenes":None,"type":"ears", "name":"Friezard"}
                },
                "00000010": {
                    "0000": {"partId":"ears-pogona", "class":"reptile", "specialGenes":None,"type":"ears", "name":"Pogona"},
                    "0001": {"partId":"ears-deadly-pogona", "class":"reptile", "specialGenes":"mystic", "type":"ears", "name":"Deadly Pogona"}
                },
                "00001010": {
                    "0000": {"partId":"ears-swirl", "class":"reptile", "specialGenes":None,"type":"ears", "name":"Swirl"}
                },
                "00001100": {"0000": {"partId":"ears-sidebarb", "class":"reptile", "specialGenes":None,"type":"ears", "name":"Sidebarb"}
                }
            },
            "back": {
                "00001000": {
                    "0000": {"partId":"back-indian-star", "class":"reptile", "specialGenes":None,"type":"back", "name":"Indian Star"},
                    "0101": {"partId":"back-frozen-bucket", "class":"reptile", "specialGenes":"xmas","type":"back", "name":"Frozen Bucket"}
                },
                "00000010": {
                    "0000": {"partId":"back-bone-sail", "class":"reptile", "specialGenes":None,"type":"back", "name":"Bone Sail"},
                    "0001": {"partId":"back-rugged-sail", "class":"reptile", "specialGenes":"mystic", "type":"back", "name":"Rugged Sail"}
                },
                "00000100": {
                    "0000": {"partId":"back-tri-spikes", "class":"reptile", "specialGenes":None,"type":"back", "name":"Tri Spikes"}
                },
                "00000110": {
                    "0000": {"partId":"back-green-thorns", "class":"reptile", "specialGenes":None,"type":"back", "name":"Green Thorns"}
                },
                "00001010": {
                    "0000": {"partId":"back-red-ear", "class":"reptile", "specialGenes":None,"type":"back", "name":"Red Ear"},
                    "0110": {"partId":"back-turtle-buoy", "class":"reptile", "name":"Turtle Buoy", "specialGenes":"summer", "type":"back"},
                    "1001": {"partId":"back-turtle-buoy-shiny", "class":"reptile", "name":"Turtle Buoy Shiny", "specialGenes":"shiny", "type":"back"}
                },
                "00001100": {
                    "0000": {"partId":"back-croc", "class":"reptile", "specialGenes":None,"type":"back", "name":"Croc"}
                }
            },
            "tail": {
                "00000100": {
                    "0000": {"partId":"tail-iguana", "class":"reptile", "specialGenes":None,"type":"tail", "name":"Iguana"}
                },
                "00000010": {
                    "0000": {"partId":"tail-wall-gecko", "class":"reptile", "specialGenes":None,"type":"tail", "name":"Wall Gecko"},
                    "0001": {"partId":"tail-escaped-gecko", "class":"reptile", "specialGenes":"mystic", "type":"tail", "name":"Escaped Gecko"}
                },
                "00000110": {
                    "0000": {"partId":"tail-tiny-dino", "class":"reptile", "specialGenes":None,"type":"tail", "name":"Tiny Dino"},
                    "0101": {"partId":"tail-fir-trunk", "class":"reptile", "specialGenes":"xmas","type":"tail", "name":"Fir Trunk"}
                },
                "00001000": {
                    "0000": {"partId":"tail-snake-jar", "class":"reptile", "specialGenes":None,"type":"tail", "name":"Snake Jar"},
                    "0100": {"partId":"tail-december-surprise", "class":"reptile", "specialGenes":"xmas", "type":"tail", "name":"December Surprise"}
                },
                "00001010": {
                    "0000": {"partId":"tail-gila", "class":"reptile", "specialGenes":None,"type":"tail", "name":"Gila"}
                },
                "00001100": {
                    "0000": {"partId":"tail-grass-snake", "class":"reptile", "specialGenes":None,"type":"tail", "name":"Grass Snake"}
                }
            },
            "horn": {
                "00000010": {
                    "0000": {"partId":"horn-unko", "class":"reptile", "specialGenes":None,"type":"horn", "name":"Unko"},
                    "0001": {"partId":"horn-pinku-unko", "class":"reptile", "specialGenes":"mystic", "type":"horn", "name":"Pinku Unko"},
                    "0111": {"partId":"horn-strawberry-ice-cream", "class":"reptile", "name":"Strawberry Ice Cream", "specialGenes":"summer", "type":"horn"},
                    "1010": {"partId":"horn-strawberry-ice-cream-shiny", "class":"reptile", "name":"Strawberry Ice Cream Shiny", "specialGenes":"shiny", "type":"horn"},
                    "0110": {"partId":"horn-watermelon-ice-cream", "class":"reptile", "name":"Watermelon Ice Cream", "specialGenes":"summer", "type":"horn"},
                    "1001": {"partId":"horn-watermelon-ice-cream-shiny", "class":"reptile", "name":"Watermelon Ice Cream Shiny", "specialGenes":"shiny", "type":"horn"},
                    "1000": {"partId":"horn-vanilla-ice-cream", "class":"reptile", "name":"Vanilla Ice Cream", "specialGenes":"summer", "type":"horn"},
                    "1011": {"partId":"horn-vanilla-ice-cream-shiny", "class":"reptile", "name":"Vanilla Ice Cream Shiny", "specialGenes":"shiny", "type":"horn"}
                },
                "00000110": {
                    "0000": {"partId":"horn-cerastes", "class":"reptile", "specialGenes":None,"type":"horn", "name":"Cerastes"}
                },
                "00000100": {
                    "0000": {"partId":"horn-scaly-spear", "class":"reptile", "specialGenes":None,"type":"horn", "name":"Scaly Spear"}
                },
                "00001010": {
                    "0000": {"partId":"horn-incisor", "class":"reptile", "specialGenes":None,"type":"horn", "name":"Incisor"}
                },
                "00001000": {
                    "0000": {"partId":"horn-scaly-spoon", "class":"reptile", "specialGenes":None,"type":"horn", "name":"Scaly Spoon"}
                },
                "00001100": {
                    "0000": {"partId":"horn-bumpy", "class":"reptile", "specialGenes":None,"type":"horn", "name":"Bumpy"}
                }
            }
        },
        "plant": {
            "tail": {
                "00001000": {
                    "0000": {"partId":"tail-yam", "class":"plant", "specialGenes":None,"type":"tail", "name":"Yam"}
                },
                "00000010": {
                    "0000": {"partId":"tail-carrot", "class":"plant", "specialGenes":None,"type":"tail", "name":"Carrot"},
                    "0001": {"partId":"tail-namek-carrot", "class":"plant", "specialGenes":"mystic", "type":"tail", "name":"Namek Carrot"}
                },
                "00000100": {
                    "0000": {"partId":"tail-cattail", "class":"plant", "specialGenes":None,"type":"tail", "name":"Cattail"}
                },
                "00000110": {
                    "0000": {"partId":"tail-hatsune", "class":"plant", "specialGenes":None,"type":"tail", "name":"Hatsune"}
                },
                "00001010": {
                    "0000": {"partId":"tail-potato-leaf", "class":"plant", "specialGenes":None,"type":"tail", "name":"Potato Leaf"}
                },
                "00001100": {
                    "0000": {"partId":"tail-hot-butt", "class":"plant", "specialGenes":None,"type":"tail", "name":"Hot Butt"}
                }
            },
            "mouth": {
                "00000100": {
                    "0000": {"partId":"mouth-zigzag", "class":"plant", "specialGenes":None,"type":"mouth", "name":"Zigzag"},
                    "0100": {"partId":"mouth-rudolph", "class":"plant", "specialGenes":"xmas", "type":"mouth", "name":"Rudolph"}
                },
                "00000010": {
                    "0000": {"partId":"mouth-serious", "class":"plant", "specialGenes":None,"type":"mouth", "name":"Serious"},
                    "0001": {"partId":"mouth-humorless", "class":"plant", "specialGenes":"mystic", "type":"mouth", "name":"Humorless"}
                },
                "00001000": {
                    "0000": {"partId":"mouth-herbivore", "class":"plant", "specialGenes":None,"type":"mouth", "name":"Herbivore"}
                },
                "00001010": {
                    "0000": {"partId":"mouth-silence-whisper", "class":"plant", "specialGenes":None,"type":"mouth", "name":"Silence Whisper"}
                }
            },
            "eyes": {
                "00000010": {
                    "0000": {"partId":"eyes-papi", "class":"plant", "specialGenes":None,"type":"eyes", "name":"Papi"},
                    "0001": {"partId":"eyes-dreamy-papi", "class":"plant", "specialGenes":"mystic", "type":"eyes", "name":"Dreamy Papi"}
                },
                "00000100": {
                    "0000": {"partId":"eyes-confused", "class":"plant", "specialGenes":None,"type":"eyes", "name":"Confused"}
                },
                "00001010": {
                    "0000": {"partId":"eyes-blossom", "class":"plant", "specialGenes":None,"type":"eyes", "name":"Blossom"}
                },
                "00001000": {
                    "0000": {"partId":"eyes-cucumber-slice", "class":"plant", "specialGenes":None,"type":"eyes", "name":"Cucumber Slice"}
                }
            },
            "ears": {
                "00000010": {
                    "0000": {"partId":"ears-leafy", "class":"plant", "specialGenes":None,"type":"ears", "name":"Leafy"},
                    "0001": {"partId":"ears-the-last-leaf", "class":"plant", "specialGenes":"mystic", "type":"ears", "name":"The Last Leaf"}
                },
                "00000110": {
                    "0000": {"partId":"ears-rosa", "class":"plant", "specialGenes":None,"type":"ears", "name":"Rosa"}
                },
                "00000100": {
                    "0000": {"partId":"ears-clover", "class":"plant", "specialGenes":None,"type":"ears", "name":"Clover"}
                },
                "00001000": {
                    "0000": {"partId":"ears-sakura", "class":"plant", "specialGenes":None,"type":"ears", "name":"Sakura"},
                    "0011": {"partId":"ears-maiko", "class":"plant", "specialGenes":"japan", "type":"ears", "name":"Maiko"}
                },
                "00001010": {
                    "0000": {"partId":"ears-hollow", "class":"plant", "specialGenes":None,"type":"ears", "name":"Hollow"},
                    "0101": {"partId":"ears-pinecones","class":"plant","specialGenes":"xmas","type":"ears","name":"Pinecones"}
                },
                "00001100": {
                    "0000": {"partId":"ears-lotus", "class":"plant", "specialGenes":None,"type":"ears", "name":"Lotus"}
                }
            },
            "back": {
                "00000110": {
                    "0000": {"partId":"back-bidens", "class":"plant", "specialGenes":None,"type":"back", "name":"Bidens"}
                },
                "00000100": {
                    "0000": {"partId":"back-shiitake", "class":"plant", "specialGenes":None,"type":"back", "name":"Shiitake"},
                    "0011": {"partId":"back-yakitori", "class":"plant", "specialGenes":"japan", "type":"back", "name":"Yakitori"}
                },
                "00000010": {
                    "0000": {"partId":"back-turnip", "class":"plant", "specialGenes":None,"type":"back", "name":"Turnip"},
                    "0001": {"partId":"back-pink-turnip", "class":"plant", "specialGenes":"mystic", "type":"back", "name":"Pink Turnip"}
                },
                "00001010": {
                    "0000": {"partId":"back-mint", "class":"plant", "specialGenes":None,"type":"back", "name":"Mint"}
                },
                "00001000": {
                    "0000": {"partId":"back-watering-can", "class":"plant", "specialGenes":None,"type":"back", "name":"Watering Can"}
                },
                "00001100": {
                    "0000": {"partId":"back-pumpkin", "class":"plant", "specialGenes":None,"type":"back", "name":"Pumpkin"}
                }
            },
            "horn": {
                "00000100": {
                    "0000": {"partId":"horn-beech", "class":"plant", "specialGenes":None,"type":"horn", "name":"Beech"},
                    "0011": {"partId":"horn-yorishiro", "class":"plant", "specialGenes":"japan", "type":"horn", "name":"Yorishiro"}
                },
                "00000110": {
                    "0000": {"partId":"horn-rose-bud", "class":"plant", "specialGenes":None,"type":"horn", "name":"Rose Bud"}
                },
                "00000010": {
                    "0000": {"partId":"horn-bamboo-shoot", "class":"plant", "specialGenes":None,"type":"horn", "name":"Bamboo Shoot"},
                    "0001": {"partId":"horn-golden-bamboo-shoot", "class":"plant", "specialGenes":"mystic", "type":"horn", "name":"Golden Bamboo Shoot"}
                },
                "00001010": {
                    "0000": {"partId":"horn-cactus", "class":"plant", "specialGenes":None,"type":"horn", "name":"Cactus"}
                },
                "00001000": {
                    "0000": {"partId":"horn-strawberry-shortcake", "class":"plant", "specialGenes":None,"type":"horn", "name":"Strawberry Shortcake"}
                },
                "00001100": {
                    "0000": {"partId":"horn-watermelon", "class":"plant", "specialGenes":None,"type":"horn", "name":"Watermelon"}
                }
            }
        }
    }
    classGeneMap = {
        "00000": "beast",
        "00001": "bug",
        "00010": "bird",
        "00011": "plant",
        "00100": "aquatic",
        "00101": "reptile",
        "10000": "mech",
        "10001": "dawn",
        "10010": "dusk"
    }

    def getTraits(genes):
        groups = [
            genes[0:128],
            genes[128:192],
            genes[192:256],
            genes[256:320],
            genes[320:384],
            genes[384:448],
            genes[448:512]
        ]

        eyes = getPartsFromGroup("eyes", groups[1])
        mouth = getPartsFromGroup("mouth", groups[2])
        ears = getPartsFromGroup("ears", groups[3])
        horn = getPartsFromGroup("horn", groups[4])
        back = getPartsFromGroup("back", groups[5])
        tail = getPartsFromGroup("tail", groups[6])

        data_set = {"eyes": eyes, "ears": ears, "mouth": mouth, "horn": horn, "back": back, "tail": tail}
        return json.dumps(data_set)

    genesConcat = ("0" * (512 - len(str(bin(int(axie_genes, 16)))[2:]))) + str(bin(int(axie_genes, 16)))[2:]
    traits = getTraits(genesConcat)
    return traits

#this should be interacting with a CA to get certificate or blockchain based key distributor like dnsTurtle

server_pub_key="""-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCCR9QQ5ch3qhTd9VA4auo5T3s2\ny4AEboZSbzgeACiNg+l3S0gdfVpNyTj4I3+AGNeYIktkc5vbyuXhdc0xKY2sFOph\nxLy6Ah/n8J0fXgUuxK5TptxkNrrrJYFRDqN4BjqBDENd/Nzjx7s7gZXM4ILs+Zuq\nvxQwLwp6mUMVCLliFwIDAQAB\n-----END PUBLIC KEY-----"""
server_priv_key="""-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQCCR9QQ5ch3qhTd9VA4auo5T3s2y4AEboZSbzgeACiNg+l3S0gd\nfVpNyTj4I3+AGNeYIktkc5vbyuXhdc0xKY2sFOphxLy6Ah/n8J0fXgUuxK5Tptxk\nNrrrJYFRDqN4BjqBDENd/Nzjx7s7gZXM4ILs+ZuqvxQwLwp6mUMVCLliFwIDAQAB\nAoGAHI9ghv/IrasEfhAMMQIHLN8mtMFx5AbSvXmSRMlmGnfjk3pWadiUFl9ZdNRb\nXBqWEMzb2D6b2VgmgwGPJQrl+pZcrx4DP26kb3uceLcex6iyjDRJ59+N+pmTd8bU\nD2nmekuK9ZgS5Zek3mP98dNbCFPtrJwPFyUftbAjl3ozsFECQQC1mqHw3dk49nyj\nAKvTstb8SRfxF7Z2fqbFnGgDE/valDOf3LNnlE3vjpH4sAuqfAR3JZhIdiXs3Zb3\nshsLhfI/AkEAt6a/wwH5CfPfOvAjuF+6hmjRCG1GiY1/192dwZksjsI4gQfMMD5G\nOKLezAzDTuwPrPVk81E8+/j8prFuWSjqKQJBAJDCt436OdqXWRjSQyXYbFjkpwoO\n3eqs4KGrIJo7hspg0pn+4p+Rb2KjIia7pkD65NBZDn/MdkTPCjVeKwLPfh8CQQCQ\nVIMmTbmbwcYxOqLH9qvPkDafacnitoq/apLdoHStKSRg+3DUhUyInC9+q5UexFS5\neA3DT5ge6pocoxr3BTmpAkByGMpnYxBFM5hLwXCr6E2UZnVGT23vZVRVeXyQjfrW\n6D62jHKbt7vs6tszavwi8xT655UUQPitrqwRjeQUMBtC\n-----END RSA PRIVATE KEY-----"""

client_priv_key="""-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAMeFaOLvPPVUEegy
JfNpeY5ZywZNRuSpaS4YnMAaFQHFeTIFz0iwou7GsIX/C4mURJseha8va30YcchG
SmFH5UdWW915l58PvOShFW7coCBim/xsaJVyxNAHBT/xu1aRUtDyAiUkwu3OXKF8
jMejQ7ZnYtFS9qR8m/qbqQyZwo4JAgMBAAECgYAfO4gOtiqRsMZY1bjRILqxiOba
JrCpTMe1Oo8XFz4gl9v/857eHyByRlINt74DnF0c9yswIDkwTOpK0o4EKm/+cs8Y
uKtT/zU3L9aNMGabgZ6Spz6dAnn4yu8B5aZc1EDG7gadG9KTSD6ikfRYyNirAwQk
Kjwd3SD+C7Kh3ZtiDQJBAPTl6fXm1rPbSxlaTlBhX6bfGL0OiwTuJkUmg0xGN99u
pJgQhwkFv+XjI/Q2bjaoyMgV4n2TR2QHBOs5gimpWHsCQQDQkONTR3Yfg1CW1aCW
IcJMvefbVqQET066g4Kpl+S2SwC8uNHTlK1GugzaFnML/4UmJYBnb2ONix+k4+LE
nEZLAkEA0ZublUG/kG9opsl5cCj3sp8O0HoLGOwwy0z8YiNTnSRZMmIrAdju93dj
BZo02Qm72C2LDoopN38egapWMwxj0wJAZqydLJdGgHb9ynN6bc5Kv8rRhHofnnuI
b2tkfKbpEhDUWRPHQBi2QNZAk3BvzJ1K6B+YGdONN9YgiuUg8tdYBwJAAkRIa8ym
TFKYU5DBoa7Ec2gTxSHIXINxiZSxkzgIxQUBYlH/SzzhFKoq41tIJkkv0KvM1dhl
XMMo4j1sImdAuA==
-----END PRIVATE KEY-----
"""

client_pub_key="""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHhWji7zz1VBHoMiXzaXmOWcsG
TUbkqWkuGJzAGhUBxXkyBc9IsKLuxrCF/wuJlESbHoWvL2t9GHHIRkphR+VHVlvd
eZefD7zkoRVu3KAgYpv8bGiVcsTQBwU/8btWkVLQ8gIlJMLtzlyhfIzHo0O2Z2LR
UvakfJv6m6kMmcKOCQIDAQAB
-----END PUBLIC KEY-----"""

owner_block_chain_address = [
    {
        "address" : "17fx42zBZbz69bzjC2eZShj5Zy5RMReZQD",
        "pubkey" : "0262440ddc2ce39717c5b083f481a9c7abfc9d992162d0b4344e2a6649e04d815d",
        "privkey" : "KxGwUtx4d5Avr83xS2Hk4kuC666xttDU34L8AFwY9VFUitWR8QPs2"
    }
]

device_block_chain_address = [
    {
        "address" : "1EtA42RsVudTfTkLHqAuQTmb3YxTRWqRZv",
        "pubkey" : "027b91c85c8d93a2d513a6e9eac04706d785068b3366f6f092b06119d8aa49d9da",
        "privkey" : "KyZSJ7D9ioaM7SuggdEH5TpgfEHddsbcoGaEeg3d3uivi5KBDtHx"
    }
]

test_address = [
    {
        "address" : "1LYqktdzYjCEtbiWQTQ69P82tJpmVJWQ2c",
        "pubkey" : "024a730a884512278713321cb4d6b32c4dbbeb6d3b1be25346a493e9a01d964264",
        "privkey" : "L1dtN5CC2tX2SREvJysAHrgj5gH1yyDLUyxYXiAbNEYXjPjRZjUp"
    }
]

#as of now ownership belongs to  1LYqktdzYjCEtbiWQTQ69P82tJpmVJWQ2c, for further testing keep chaning the address
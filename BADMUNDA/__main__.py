import uvloop  # Comment it out if using on windows
from BADMUNDA.bot_class import BAD

if __name__ == "__main__":
    uvloop.install() # Comment it out if using on windows
    BAD().run()
    
    

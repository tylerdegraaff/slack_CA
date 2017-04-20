from slack_ca.externals.google_agenda import GoogleagendaDataAcquisition

def get_aqcuistion(command):
    """
    Get the used the keyword and pass it to the right
    acquistion.
    """
    # Read the command and return the right function
    if command == 'agenda':
        return GoogleagendaDataAcquisition()
    else:
        return "I cant find that command, please try a different one."

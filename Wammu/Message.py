import Wammu.Thread
import Wammu.Utils
import gammu

class GetMessage(Wammu.Thread.Thread):
    def run(self):
        self.ShowProgress(0)
        
        try:
            status = self.sm.GetSMSStatus()
        except gammu.GSMError, val:
            self.ShowError(val[0], True)
            return
 
        total = remain = status['SIMUsed'] + status['PhoneUsed']

        data = []
        start = True
        
        while remain > 0:
            self.ShowProgress(100 * (total - remain) / total)
            if self.canceled:
                self.Canceled()
                return
            try:
                if start:
                    value = self.sm.GetNextSMS(Start = True, Folder = 0)
                    start = False
                else:
                    value = self.sm.GetNextSMS(Location = value[0]['Location'], Folder = 0)
            except gammu.GSMError, val:
                self.ShowError(val[0], True)
                return
            data.append(value)
            remain = remain - 1

        read = []
        unread = []
        sent = []
        unsent = []
        data = gammu.LinkSMS(data)
        
        for x in data:
            i = {}
            print x
            v = gammu.DecodeSMS(x)
            print v
            i['SMS'] = x
            if v != None:
                i['SMSInfo'] = v
            Wammu.Utils.ParseMessage(i, (v != None))
            if i['State'] == 'Read':
                read.append(i)
            elif i['State'] == 'UnRead':
                unread.append(i)
            elif i['State'] == 'Sent':
                sent.append(i)
            elif i['State'] == 'UnSent':
                unsent.append(i)
                
        self.SendData(['message', ' R'], read, False)
        self.SendData(['message', 'UR'], unread, False)
        self.SendData(['message', ' S'], sent, False)
        self.SendData(['message', 'US'], unsent)

        self.ShowProgress(100)


from page import page
from frame import frame
from dm import diskManager


class BufferPoolFullError(Exception):
    # exception used in the Clock class
    def __init__(self, message):
        self.message = "buffer pool is full"


class clock:
    def __init__(self):
        # do the required initializations
        self.location = 0

    def pickVictim(self, buffer):
        # find a victim page using the clock algorithm and return the frame number
        # if all pages in the buffer pool are pinned, raise the exception BufferPoolFullError
        startLocation = self.location
        current = None

        while current!=startLocation:
            if self.location>len(buffer):
                self.location = 0
            current = self.location
            for i in range (0,startLocation):
                if buffer[i].pinCount == 0 and buffer[i].referenced ==0:
                    self.location+=1
                    return buffer[i]    #this is victim
                elif buffer[i].pinCount == 0 and buffer[i].referenced ==1:
                    buffer[i].referenced = 0
                    self.location +=1
                    current+=1
                elif buffer[i].pinCount >= 1:
                    self.location +=1
                    current+=1
            for i in range(startLocation,len(buffer)):
                if buffer[i].pinCount == 0 and buffer[i].referenced ==0:
                    self.location+=1
                    return buffer[i]    #this is victim
                elif buffer[i].pinCount == 0 and buffer[i].referenced ==1:
                    buffer[i].referenced = 0
                    self.location +=1
                    current+=1
                elif buffer[i].pinCount >= 1:
                    self.location +=1
                    current+=1

        #raise BufferPoolFullError ##I'm not calling this correctly, WILL??
    # pass


# ==================================================================================================

class bufferManager:

    def __init__(self, size):
        self.buffer = []
        self.clk = clock()
        self.dm = diskManager()
        for i in range(size):
            self.buffer.append(frame())  # creating buffer frames (i.e., allocating memory)
            self.buffer[i].frameNumber = i

    # ------------------------------------------------------------

    def pin(self, pageNumber, new=False):
        # given a page number, pin the page in the buffer
        # if new = True, the page is new so no need to read it from disk
        # if new = False, the page already exists. So read it from disk if it is not already in the pool.
        for i in range(len(self.buffer)):
            if self.buffer[i].currentPage.pageNo == pageNumber:  # already contains pageNumber
                self.buffer[i].pinCount += 1
                return self.buffer[i]
        # else it doesn't already contain pageNumber
        # find frame # that matches victim
        # frameToPin = self.buffer[0] #placeholder
        for i in range(len(self.buffer)):
            if self.buffer[i] == self.clk.pickVictim(self.buffer):
                #frameToPin = self.buffer[i]
                if self.buffer[i].dirtyBit == True:
                    self.dm.writePageToDisk(self.buffer[i].currentPage)
                # if page is not new, read page pageNo from disk into frame
                if new == False:
                    self.buffer[i].currentPage.pageNo = self.dm.readPageFromDisk(self.buffer[i].currentPage.pageNo)
                    self.buffer[i].currentPage.content = self.dm.readPageFromDisk(self.buffer[i].currentPage.content)
                else:
                    # page is new
                    self.buffer[i].pageNo = pageNumber
                self.buffer[i].pinCount = 1
                self.buffer[i].dirtyBit = False
                return self.buffer[i]

    # pass

    # ------------------------------------------------------------
    def unpin(self, pageNumber, dirty):
        pass

    def flushPage(self, pageNumber):
        # Ignore this function, it is not needed for this homework.
        # flushPage forces a page in the buffer pool to be written to disk
        for i in range(len(self.buffer)):
            if self.buffer[i].currentPage.pageNo == pageNumber:
                self.dm.writePageToDisk(self.buffer[i].currentPage)  # flush writes a page to disk
                self.buffer[i].dirtyBit = False

    def printBufferContent(self):  # helper function to display buffer content on the screen (helpful for debugging)
        print("---------------------------------------------------")
        for i in range(len(self.buffer)):
            print("frame#={} pinCount={} dirtyBit={} referenced={} pageNo={} pageContent={} ".format(
                self.buffer[i].frameNumber, self.buffer[i].pinCount, self.buffer[i].dirtyBit, self.buffer[i].referenced,
                self.buffer[i].currentPage.pageNo, self.buffer[i].currentPage.content))
        print("---------------------------------------------------")

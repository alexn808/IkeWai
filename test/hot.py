import Adafruit_MCP9808.MCP9808 as MCP9808
mcp9808 = MCP9808.MCP9808()
temp = mcp9808.readTempC()

for i in range (0,1):
    # print temp - comment out later
    print("temp: " + str(temp))

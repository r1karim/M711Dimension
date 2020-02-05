require("m711lib")


print("gamemode has been loaded")

OnPlayerConnect = function()
	print("A player has connected.")
	SendMessageToAllPlayers("test")
end
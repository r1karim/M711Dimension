require("m711lib")

print("gamemode has been loaded")

OnPlayerConnect = function(player)
	SendMessageToAllPlayers("A player has joined the game!")
end
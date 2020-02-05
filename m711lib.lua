function SendMessageToAllPlayers(fmessage)
	code = string.format("SendAllPlayersMessage('%s')", fmessage)
	python.eval(code)
end
function SendMessageToPlayer(playerid, message)
	--Nothing to be done...
end
local OnPlayerConnect
function SendMessageToAllPlayers(fmessage)
	--str = 'SendAllPlayersMessage('..fmessage..')'
	str = 'print('..fmessage..')'
	python.eval(str)
end
function SendMessageToPlayer(playerid, message)
	--Nothing to be done...
end
local OnPlayerConnect
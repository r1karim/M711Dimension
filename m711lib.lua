local OnPlayerConnect
local OnPlayerEnterCheckPoint
local OnPlayerText
function SendAllPlayersMessage(message)
	python.eval(string.format("SendAllPlayersMessage('%s')", message))
end
function SendPlayerMessage(playerid, message)
	python.eval(string.format("SendPlayerMessage(%d,'%s')", playerid,message))
end
function GetPlayerName(playerid)
	name=python.eval(string.format("GetPlayerName(%d)", playerid))
	return name
end
function SetPlayerTeam(playerid, teamid)
	--pass
end
function ShowPlayerDialog(playerid, type, title, content)
	python.eval(string.format("ShowPlayerDialog(%d, %d,'%s', '%s')", playerid, type, title, content))
end
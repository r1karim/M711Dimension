local OnPlayerConnect
local OnPlayerEnterCheckPoint
local OnPlayerText
local OnDialogResponse
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
function ShowPlayerDialog(playerid, type, dialogid,title, content, button1, button2)
	python.eval(string.format("ShowPlayerDialog(%d, %d,%d,'%s', '%s','%s','%s')", playerid, type, dialogid,title, content,button1,button2))
end
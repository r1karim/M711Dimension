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
	python.eval(string.format("SetPlayerTeam(%d, %d)", playerid, teamid))
end
function SetPlayerSkin(playerid, skinid)
	python.eval(string.format("SetPlayerSkin(%d,%d)", playerid, skinid))
end
function SetPlayerAdmin(playerid, a) -- 1 = admin
	python.eval(string.format("SetPlayerAdmin(%d, %d)", playerid, a))
end
function KickPlayer(playerid)
	python.eval(string.format("KickPlayer(%d)", playerid))
end
function GetPlayerIp(playerid)
	return python.eval(string.format("GetPlayerIp(%d)", playerid))
end
function ShowPlayerDialog(playerid, type, dialogid,title, content, button1, button2) -- The dialog id has to be only one character.
	python.eval(string.format("ShowPlayerDialog(%d, %d,%d,'%s', '%s','%s','%s')", playerid, type, dialogid,title, content,button1,button2))
end
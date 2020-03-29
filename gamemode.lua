require("m711lib")

print("gamemode has been loaded")

local RULES_DIALOG = 0

OnPlayerConnect = function(playerid)
	local playername = GetPlayerName(playerid)
	SendAllPlayersMessage(playername.." has joined the game.")
	SendPlayerMessage(playerid, string.format("Welcome to the server %s.", playername))
	ShowPlayerDialog(playerid, 0, RULES_DIALOG,"Rules", "[Insert rules here]", "okay", '')
end
OnPlayerText = function(playerid,text)
	return 1 --return (-1) to prevent the text from being sent.
end
OnDialogResponse = function(playerid, dialogid,response)
	if dialogid == RULES_DIALOG then
		if response == 0 then
			SendAllPlayersMessage(playername.. " has accepted the rules.")
		elseif response == 1 then
			SendAllPlayersMessage(playername.. " has been kicked for not accepting the rules.")
		end
	end
end
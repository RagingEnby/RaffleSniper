# RaffleSniper
A highly customizable, discord webhook based, AH tracker for items obtained in the Hypixel Year 300 raffle.

# How it works
All items obtained from the raffle, whether they be a jerry box or divans alloy, contain a special NBT tag called `raffle_year` and `raffle_win`. For example, here is a normal jerry box and one obtained from a raffle:
```
ExtraAttributes: {
  id: "JERRY_BOX_PURPLE"
}
```

```
ExtraAttributes: {
  raffle_year: 300,
  raffle_win: "year_300_small_5",
  id: "JERRY_BOX_PURPLE"
}
```
RaffleSniper will filter through every new auction on the auction house. It will decode their item bytes and check for these tags. If found, it will send to the webhook specified in config.json!

# Instructions
1. Install the dependencies **(TUTORIAL COMING SOON)**
2. Create a new channel for the messages to go to.
3. In this channel, create new discord webhook.
4. Paste this Webhook URL into to `DEFAULT` webhook in `config.json` - > `webhooks`
4.5 You may optionally do the same for:
  `LOG_WEBHOOK` (sends debug logs to discord)
  `DYE` which will send any dyes obtained from the raffle
   additionaly, you can add custom item webhooks (useful for filtering stuff like fruit bowls out of your main channel) by making new field with their item id and webhook like this:
   `"ITEM_ID": "CUSTOM_WEBHOOK"`
5. Start the bot with `python3 main.py`!
# Discord
If you have any questions or need any help with RaffleSniper, open a ticket here on github, or join [My Discord!](https://discord.gg/9sGaFGPEnE)

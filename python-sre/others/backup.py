# print(f"Database list: {mongo_client.list_database_names()}")
    # print(f"Collections names: {database.list_collection_names()}")

    # print(f"searching for keywords: {sys.argv[1]}")
    # keyword = sys.argv[1]

    # tweets_data_list = []
    # for tweet in public_tweets:
    #     print("========= INICIO ===========")
    #     print("")

    #     retuitado = "retweeted_status" in dir(tweet)
    #     print(f"Usuário: {tweet.user.name}")
    #     print(f"Retuitado: {retuitado}")
    #     print(f"Location: {tweet.user.location}")
    #     print(tweet.full_text)

    #     print("### hashtags ###")
    #     print("")

    #     if len(tweet.entities["hashtags"]) > 0:
    #         for hashtag in tweet.entities["hashtags"]:
    #             print(hashtag["text"])
    #     else:
    #         print("No hashtags found")

    #     print("")
    #     print("################")

    #     if "retweeted_status" in dir(tweet):
    #         print(f"Retuite: {tweet.retweeted_status.full_text}")

    #         tweet_status = api.get_status(tweet.id)
    #         print(f"Seguidores de {tweet.user.name}: {tweet.user.followers_count}")
    #         print("========= FIM ===========")
    #         print("")

    #         tweets_data_list.append(tweets_data)

    # tweets_table.drop()

    # # filter_result = filter(filter_by_item, tweets_data_list)
    # new_tweets_to_insert = []
    # print("========== tweets not in database ===========")
    # print(len(tweets_data_list))
    # for filtered_item in tweets_data_list:
    #     new_tweets_to_insert.append(filtered_item)

    # if len(new_tweets_to_insert) > 0:
    #     inserted_tweets = tweets_table.insert_many(new_tweets_to_insert)
    #     print(f"inserted rows: {len(inserted_tweets.inserted_ids)}")

    # users_with_top_followers = tweets_table.find().sort("Followers", -1).limit(5)

    # for top_user in users_with_top_followers:
    #     tuser = top_user["User"]
    #     tfollowers = top_user["Followers"]
    #     tdate = top_user["Date"]
    #     tlocation = top_user["UserLocation"]
    #     print(
    #         f"Usuário {tuser} é de {tlocation} e tem {tfollowers} seguidores e criou o tweet as {tdate}"
    #     )

    # print("--------- all horas -----------")

    # for tweet in tweets_data_list:
    #     print(str(tweet["Date"]) + " " + str(tweet["Language"]) + " " + str(tweet["UserLocation"]))

    # print("---------- tweets por hora ----------")

    # for agi in agg_result:
    #     print(agi)
library(tidyverse)
library(dplyr)
library(rio)
library(ggplot2)
library(readr)

score_df <- function(my_df, y_par) {
  calc_perc <- function(df) {
    return(df[2] / (df[1] + df[2]))
  }
  return((my_df[y_par] == my_df["prediction"]) %>%
    table() %>%
    calc_perc() %>%
    unname())
}

calculate_ROI_apply <- function(x, y_par) { # nolint
  if (y_par == "OvUnB") {
    if (x["prediction"] == x["OvUnB"]) {
      if (x["prediction"] == 1) {
        return(x["AvgO25"])
      } else {
        return(x["AvgU25"])
      }
    } else {
      return(0)
    }
  }

  if (y_par == "FTRB") {
    if (x["prediction"] == x["FTRB"]) {
      if (x["prediction"] == 0) {
        return(x["AvgH"])
      } else if (x["prediction"] == 1) {
        return(x["AvgD"])
      } else {
        return(x["AvgA"])
      }
    } else {
      return(0)
    }
  }
}

prepare_dataframe <- function(df, y_par) {
  # Preprocess data
  add_odds_predicted <- function(x) {
    return(x[paste("odds_", x["prediction"], sep = "")])
  }

  if (y_par == "OvUnB") {
    add_predicted_prob <- function(x) {
      return(max(x["prob_0_xgb"], x["prob_1_xgb"]))
    }

    df["prediction_prob"] <- apply(df, 1, add_predicted_prob)
    df["odds_1"] <- df["AvgO25"]
    df["odds_0"] <- df["AvgU25"]
    df["prediction_odds"] <- apply(df, 1, add_odds_predicted)
    df["payout"] <- 1 / (1 / df["odds_1"] + 1 / df["odds_0"])
    return(df)
  }
  if (y_par == "FTRB") {
    add_predicted_prob <- function(x) {
      return(max(x["prob_0_xgb"], x["prob_1_xgb"], x["prob_2_xgb"]))
    }

    df["prediction_prob"] <- apply(df, 1, add_predicted_prob)
    df["odds_0"] <- df["AvgH"]
    df["odds_1"] <- df["AvgD"]
    df["odds_2"] <- df["AvgA"]
    df["prediction_odds"] <- apply(df, 1, add_odds_predicted)
    df["payout"] <- 1 / (1 / df["odds_1"] + 1 / df["odds_0"] + 1 / df["odds_2"])
    return(df)
  }
}

histogram_util <-
  function(df, title, vlines = FALSE, prob_high = "", prob_low = "") {
    perc_test <- df$prediction %>%
      table() %>%
      prop.table() %>%
      round(2) * 100

    p1 <- ggplot(df) +
      geom_histogram(aes(x = prediction_prob), # nolint
        binwidth = 0.025
      ) +
      theme_bw() +
      ggtitle(paste(title, paste("Predicted ", perc_test %>% names(), ": ",
        perc_test, "%",
        sep = "",
        collapse = ". "
      )))

    if (vlines) {
      p1 <- p1 + geom_vline(
        xintercept = prob_low, color = "red",
        linetype = "longdash", linewidth = 1
      ) +
        geom_vline(
          xintercept = prob_high, color = "red",
          linetype = "longdash", linewidth = 1
        )
    }

    return(p1)
  }

select_games <- function(my_df, confidence_over_odds = "", min_confidence = "",
                         max_confidence = "", min_odds = "", max_odds = "",
                         min_payout = "", max_payout = "", only_0_1 = "All") {
  # all numbers

  if (confidence_over_odds != "") {
    my_df <- my_df %>% dplyr::filter(
      prediction_prob > (1 / as.numeric(prediction_odds) + confidence_over_odds) # nolint
    )
  }

  if (min_payout != "") {
    my_df <- my_df %>% dplyr::filter(payout %>% as.numeric() > min_payout) # nolint
  }

  if (max_payout != "") {
    my_df <- my_df %>% dplyr::filter(payout %>% as.numeric() < max_payout) # nolint
  }

  if (min_confidence != "") {
    my_df <- my_df %>% dplyr::filter(prediction_prob %>% as.numeric() > min_confidence) # nolint
  }

  if (max_confidence != "") {
    my_df <- my_df %>% dplyr::filter(prediction_prob %>% as.numeric() < max_confidence) # nolint
  }

  if (min_odds != "") {
    my_df <- my_df %>% dplyr::filter(prediction_odds %>% as.numeric() > min_odds) # nolint
  }

  if (max_odds != "") {
    my_df <- my_df %>% dplyr::filter(prediction_odds %>% as.numeric() < max_odds) # nolint
  }

  if (only_0_1 != "All") {
    my_df <- my_df %>% dplyr::filter(prediction == only_0_1) # nolint
  }

  return(my_df)
}

update_results <- function() {
  betting_log <- rio::import("./data/betting_log.csv")

  directory <- "./data/relevant_data/"
  files <- list.files(path = directory)
  files <- files[grepl("2223", files)]

  big_df <- rio::import(
    paste(directory, files[1], sep = "")
  )[c("Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR")]
  k <- 1
  for (file in files) {
    if (k != 1) {
      big_df <- rbind(big_df, rio::import(
        paste(directory, file, sep = "")
      )[c("Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR")])
    }
    k <- k + 1
  }

  big_df["TG"] <- big_df["FTHG"] + big_df["FTAG"]
  big_df["OvUnB"] <- apply(big_df, 1, function(x) {
    ifelse(x[["TG"]] %>% as.numeric() > 2.5, 1, 0)
  })
  big_df["Date"] <- apply(
    big_df,
    1, function(x) toString(as.Date(x["Date"], "%d/%m/%Y"))
  )
  big_df["GameIndex"] <- apply(
    big_df,
    1, function(x) paste(x["Date"], x["HomeTeam"], x["AwayTeam"], sep = "_")
  )
  common_indices <- intersect(big_df$GameIndex, betting_log$GameIndex)

  for (ci in common_indices) {
    betting_log[which(betting_log == ci), ]["result"] <-
      dplyr::filter(big_df, GameIndex == ci)["OvUnB"] # nolint
  }
  write.csv(betting_log, "./data/betting_log.csv", row.names = FALSE)
}

write_elo <- function(league) { # nolint
  start_time <- Sys.time()

  # Function 1, create from scratch
  files <- list.files("./data/all_data/")
  files_in_league <- files[startsWith(files, league)]
  years <- files_in_league %>% sapply(function(x) substr(x, 3, 7))
  years <- years[order(years %>% as.numeric())]
  data_frames <- lapply(
    files_in_league,
    function(x) rio::import(paste("./data/all_data/", x, sep = ""))
  )

  big_df <- data_frames[[1]][c(
    "Date", "HomeTeam", "AwayTeam", "FTR", "FTAG", "FTHG"
  )]
  for (df in data_frames[2:length(data_frames)]) {
    big_df <- rbind(big_df, df[c(
      "Date", "HomeTeam", "AwayTeam", "FTR", "FTAG", "FTHG"
    )])
  }

  all_teams <- c(big_df$HomeTeam, big_df$AwayTeam) %>% unique()
  all_dates <- c(big_df$Date) %>% unique()
  all_dates[[length(all_dates) + 1]] <- "last_date"

  base_list <- list()

  for (team in all_teams) {
    base_list[[team]] <- 1000
  }

  elo_list <- list()

  calculate_new_elo <- function(row, elo_last_date) {
    ht <- row$HomeTeam
    at <- row$AwayTeam

    ht_elo <- elo_last_date[[ht]]
    at_elo <- elo_last_date[[at]]

    we_ht <- 1 / (1 + 10^((at_elo - (ht_elo + 70)) / 400))
    we_at <- 1 / (1 + 10^((ht_elo - (at_elo - 70)) / 400))

    if (row["FTR"] == "H") { # nolint
      ht_res <- 1
      at_res <- 0
    } else if (row["FTR"] == "A") { # nolint
      ht_res <- 0
      at_res <- 1
    } else {
      ht_res <- 0.5
      at_res <- 0.5
    }

    ht_elo <- ht_elo + 40 * (ht_res - we_ht)
    at_elo <- at_elo + 40 * (at_res - we_at)

    teams_list <- list()
    teams_list[[ht]] <- ht_elo
    teams_list[[at]] <- at_elo
    return(teams_list)
  }

  calculate_elo_from_prev_date <- function(last_date, big_df, elo_last_date) { # nolint
    update_list <- list()
    games_last_date <- big_df %>% dplyr::filter(Date == last_date) # nolint
    for (i in seq_along(games_last_date$FTR)) {
      update_list <- append(
        update_list, calculate_new_elo(games_last_date[i, ], elo_last_date)
      )
    }
    for (team in names(update_list)) {
      elo_last_date[[team]] <- update_list[[team]]
    }
    return(elo_last_date)
  }

  first_date <- all_dates[1]
  elo_list[[first_date]] <- base_list

  for (index_date in seq_along(all_dates[2:length(all_dates)])) {
    this_date <- all_dates[index_date + 1]
    last_date <- all_dates[index_date]
    elo_list[[this_date]] <- calculate_elo_from_prev_date(
      last_date, big_df, elo_list[[last_date]]
    )
  }

  elo_list[[all_dates[[length(all_dates)]]]]

  for (file in list.files("./data/csv/")) {
    if (startsWith(file, league)) {
      elo_ht <- function(row) {
        date <- row[["Date"]]
        elo <- elo_list[[date]][[row[["HomeTeam"]]]]
        return(elo[[1]])
      }

      elo_at <- function(row) {
        date <- row[["Date"]]
        elo <- elo_list[[date]][[row[["AwayTeam"]]]]
        return(elo[[1]])
      }

      win_e_ht <- function(row) {
        elo_at <- row[["elo_at"]] %>% as.numeric()
        elo_ht <- row[["elo_ht"]] %>% as.numeric()
        we_ht <- 1 /
          (1 + 10^((elo_at - (elo_ht + 70)) / 400))
        return(we_ht)
      }

      df <- rio::import(paste("./data/csv/", file, sep = ""))
      elo_ht <- apply(df, 1, function(x) elo_ht(x))
      elo_at <- apply(df, 1, function(x) elo_at(x))
      df$elo_ht <- elo_ht
      df$elo_at <- elo_at
      win_e_ht <- apply(df, 1, function(x) win_e_ht(x))
      df$win_e_ht <- win_e_ht
      file_name <- paste("./data/csv/", file, sep = "")
      write.csv(df, file_name, row.names = FALSE)
    }
  }

  write.csv(
    elo_list[[all_dates[[length(all_dates)]]]],
    paste("./data/elo_lists/", league, ".csv", sep = ""),
    row.names = FALSE
  )

  end_time <- Sys.time()
  print(paste(
    league, " elo added: ",
    as.numeric(end_time - start_time) %>% round(2),
    " seconds",
    sep = ""
  ))
}

add_elo_to_scrape <- function() {
  df <- rio::import("./data/scrape_data/latest_scrape_prepared.csv")

  dir <- "./data/elo_lists/"
  elo_files <- list.files(dir)
  elo_df <- rio::import(paste(dir, elo_files[1], sep = ""))
  for (file in elo_files[2:length(elo_files)]) {
    elo_df <- cbind(elo_df, rio::import(paste(dir, file, sep = "")))
  }

  elo_ht <- c()
  for (ht in df$HomeTeam) {
    ht <- str_replace(ht, " ", ".") # nolint
    ht <- str_replace(ht, " ", ".") # nolint
    ht <- str_replace(ht, "'", ".") # nolint
    ht <- str_replace(ht, "'", ".") # nolint
    ht <- str_replace(ht, "-", ".") # nolint
    elo_ht <- c(elo_ht, elo_df[[ht]])
  }

  elo_at <- c()
  for (at in df$AwayTeam) {
    at <- str_replace(at, " ", ".") # nolint
    at <- str_replace(at, " ", ".") # nolint
    at <- str_replace(at, "'", ".") # nolint
    at <- str_replace(at, "'", ".") # nolint
    at <- str_replace(at, "-", ".") # nolint
    elo_at <- c(elo_at, elo_df[[at]])
  }


  win_prob_ht <- function(ht_elo, at_elo) {
    return(1 / (1 + 10^((at_elo - (ht_elo + 70)) / 400)))
  }

  win_e_ht <- c()
  for (i in seq_along(elo_ht)) {
    win_e_ht <- c(win_e_ht, win_prob_ht(elo_ht[i], elo_at[i]))
  }

  df$elo_ht <- elo_ht
  df$elo_at <- elo_at
  df$win_e_ht <- win_e_ht

  write.csv(df,
    "./data/scrape_data/latest_scrape_prepared.csv",
    row.names = FALSE
  )
}

write_tilt <- function(league) {
  start_time <- Sys.time()

  files <- list.files("./data/all_data/")
  files_in_league <- files[startsWith(files, league)]
  years <- files_in_league %>% sapply(function(x) {
    substr(x, 3, 7)
  })
  years <- years[order(years %>% as.numeric())]
  data_frames <- lapply(
    files_in_league,
    function(x) {
      rio::import(paste("./data/all_data/", x, sep = ""))
    }
  )

  big_df <-
    data_frames[[1]][c("Date", "HomeTeam", "AwayTeam", "FTR", "FTAG", "FTHG")]
  for (df in data_frames[2:length(data_frames)]) {
    big_df <-
      rbind(big_df, df[
        c("Date", "HomeTeam", "AwayTeam", "FTR", "FTAG", "FTHG")
      ])
  }

  all_teams <- c(big_df$HomeTeam, big_df$AwayTeam) %>% unique()
  all_dates <- c(big_df$Date) %>% unique()
  all_dates[[length(all_dates) + 1]] <- "last_date"
  base_list <- list()
  for (team in all_teams) {
    base_list[[team]] <- 1
  }

  tilt_list <- list()

  calculate_new_tilt <- function(row, tilt_last_date) {
    ht <- row$HomeTeam
    at <- row$AwayTeam
    tg <- row$FTAG + row$FTHG

    ht_tilt_old <- tilt_last_date[[ht]]
    at_tilt_old <- tilt_last_date[[at]]

    ht_tilt <- 0.95 * ht_tilt_old + 0.05 * tg / at_tilt_old / 2.5
    at_tilt <- 0.95 * at_tilt_old + 0.05 * tg / ht_tilt_old / 2.5

    teams_list <- list()
    teams_list[[ht]] <- ht_tilt
    teams_list[[at]] <- at_tilt
    return(teams_list)
  }

  calculate_tilt_from_prev_date <-
    function(last_date, big_df, tilt_last_date) {
      update_list <- list()
      games_last_date <-
        big_df %>% dplyr::filter(Date == last_date) # nolint
      for (i in seq_along(games_last_date$FTR)) {
        update_list <- append(
          update_list,
          calculate_new_tilt(
            games_last_date[i, ], tilt_last_date
          )
        )
      }
      for (team in names(update_list)) {
        tilt_last_date[[team]] <- update_list[[team]]
      }
      return(tilt_last_date)
    }


  first_date <- all_dates[1]
  tilt_list[[first_date]] <- base_list

  for (index_date in seq_along(all_dates[2:length(all_dates)])) {
    this_date <- all_dates[index_date + 1]
    last_date <- all_dates[index_date]
    tilt_list[[this_date]] <-
      calculate_tilt_from_prev_date(last_date, big_df, tilt_list[[last_date]])
  }

  for (file in list.files("./data/csv/")) {
    if (startsWith(file, league)) {
      tilt_ht <- function(row) {
        date <- row[["Date"]]
        tilt <- tilt_list[[date]][[row[["HomeTeam"]]]]
        return(tilt[[1]])
      }

      tilt_at <- function(row) {
        date <- row[["Date"]]
        tilt <- tilt_list[[date]][[row[["AwayTeam"]]]]
        return(tilt[[1]])
      }

      df <- rio::import(paste("./data/csv/", file, sep = ""))
      tilt_ht <- apply(df, 1, function(x) {
        tilt_ht(x)
      })
      tilt_at <- apply(df, 1, function(x) {
        tilt_at(x)
      })
      df$tilt_ht <- tilt_ht
      df$tilt_at <- tilt_at
      file_name <- paste("./data/csv/", file, sep = "")
      write.csv(df, file_name, row.names = FALSE)
    }
  }

  write.csv(tilt_list[[all_dates[[length(all_dates)]]]],
    paste("./data/tilt_lists/", league, ".csv", sep = ""),
    row.names = FALSE
  )

  end_time <- Sys.time()
  print(paste(
    league,
    " tilt added: ",
    as.numeric(end_time - start_time) %>% round(2),
    " seconds",
    sep = ""
  ))
}

apply_current_test <- function(my_df) {
  test_model_parameters <- rio::import(
    "./interface_files/current_test_parameters.json"
  )

  confidence_over_odds <- test_model_parameters$confidence_over_odds
  min_confidence <- test_model_parameters$min_confidence
  max_confidence <- test_model_parameters$max_confidence
  min_odds <- test_model_parameters$min_odds
  max_odds <- test_model_parameters$max_odds
  only_0_1 <- test_model_parameters$only_0_1

  filtered_df <- select_games(
    my_df,
    confidence_over_odds,
    min_confidence,
    max_confidence,
    min_odds,
    max_odds,
    min_payout = "",
    max_payout = "",
    only_0_1
  )

  return(filtered_df)
}

apply_existing_test <- function(my_df, test_name) {
  test_model_parameters <- rio::import(
    paste("./models_tests/saved_tests/",
      test_name, "/test_parameter.json",
      sep = ""
    )
  )

  confidence_over_odds <- test_model_parameters$confidence_over_odds
  min_confidence <- test_model_parameters$min_confidence
  max_confidence <- test_model_parameters$max_confidence
  min_odds <- test_model_parameters$min_odds
  max_odds <- test_model_parameters$max_odds
  only_0_1 <- test_model_parameters$only_0_1

  filtered_df <- select_games(
    my_df,
    confidence_over_odds,
    min_confidence,
    max_confidence,
    min_odds,
    max_odds,
    min_payout = "",
    max_payout = "",
    only_0_1
  )
  return(filtered_df)
}

add_tilt_to_scrape <- function() {
  df <- rio::import("./data/scrape_data/latest_scrape_prepared.csv")

  dir <- "./data/tilt_lists/"
  tilt_files <- list.files(dir)
  tilt_df <- rio::import(paste(dir, tilt_files[1], sep = ""))
  for (file in tilt_files[2:length(tilt_files)]) {
    tilt_df <- cbind(tilt_df, rio::import(paste(dir, file, sep = "")))
  }

  tilt_ht <- c()
  for (ht in df$HomeTeam) {
    ht <- str_replace(ht, " ", ".") # nolint
    ht <- str_replace(ht, " ", ".") # nolint
    ht <- str_replace(ht, "'", ".") # nolint
    ht <- str_replace(ht, "'", ".") # nolint
    ht <- str_replace(ht, "-", ".") # nolint
    tilt_ht <- c(tilt_ht, tilt_df[[ht]])
  }

  tilt_at <- c()
  for (at in df$AwayTeam) {
    at <- str_replace(at, " ", ".") # nolint
    at <- str_replace(at, " ", ".") # nolint
    at <- str_replace(at, "'", ".") # nolint
    at <- str_replace(at, "'", ".") # nolint
    at <- str_replace(at, "-", ".") # nolint
    tilt_at <- c(tilt_at, tilt_df[[at]])
  }

  df$tilt_ht <- tilt_ht
  df$tilt_at <- tilt_at

  write.csv(df, "./data/scrape_data/latest_scrape_prepared.csv", row.names = FALSE)
}

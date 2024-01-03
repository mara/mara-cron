# Changelog

## 0.12.0 (2024-01-03)

- use mara cli instead of flask mara commands

## 0.11.1-2 (2023-12-15)

- fix old CLI command names

## 0.11.0 (2023-12-06)

- add entry point `mara.commands` (for [mara-cli](https://github.com/mara/mara-cli) support)
- add `mara-cron` click group. Commands outside of the click group will be dropped in 1.0.0 release

## 0.10.0-1 (2023-06-27)

- add cli command `mara_cron.schedule-job` (#3)

## 0.9.6 (2022-09-30)

- allow to run disabled jobs manually via UI
- fix config.default_job_max_retries did not work

## 0.9.5 (2022-06-24)

- fix add missing `max_retries` option to job class `MaraJob`, `RunPipelineJob`

## 0.9.3-4 (2022-06-22)

- add `max_retries` option (#1)
- add option to manually execte a singe task once (with the assumtion that you will clean up the crontab file once a year (!))
- improve UI display of cron jobs
- refactoring of several functions and parameters

## 0.9.0 - 0.9.2 (2021-01-28)

- initial version

# gomidashi-feeder

```zsh
PROJECT_NAME="<YOUR_PROJECT_NAME>"
gcloud projects create ${PROJECT_NAME}

PROJECT_ID=$(gcloud projects list --filter ${PROJECT_NAME} --limit 1 | awk 'NR>1 {print $1}')
SA_NAME="<YOUR_SERVICE_ACCOUNT_NAME>"
BILLING_ACCOUNT_ID="" # TODO: gcloud beta billing accounts list


gcloud beta billing projects link ${PROJECT_ID} --billing-account=${BILLING_ACCOUNT_ID}
gcloud iam service-accounts create ${SA_NAME} --display-name ${SA_NAME}
gcloud iam service-accounts keys create ./.gcp_key.json --iam-account=${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com --role roles/editor
gcloud services enable \
  pubsub.googleapis.com \
  cloudfunctions.googleapis.com \
  cloudscheduler.googleapis.com \
  appengine.googleapis.com \
  storage-api.googleapis.com
```


## Cloud Functions のイベントタイプ

下記コマンドの ` EVENT_TYPE` を指定する。

```bash
$ gcloud functions event-types list
EVENT_PROVIDER                   EVENT_TYPE                                                EVENT_TYPE_DEFAULT  RESOURCE_TYPE       RESOURCE_OPTIONAL
cloud.pubsub                     google.pubsub.topic.publish                               Yes                 topic               No
cloud.pubsub                     providers/cloud.pubsub/eventTypes/topic.publish           No                  topic               No
cloud.storage                    google.storage.object.archive                             No                  bucket              No
cloud.storage                    google.storage.object.delete                              No                  bucket              No
cloud.storage                    google.storage.object.finalize                            Yes                 bucket              No
cloud.storage                    google.storage.object.metadataUpdate                      No                  bucket              No
cloud.storage                    providers/cloud.storage/eventTypes/object.change          No                  bucket              No
google.firebase.analytics.event  providers/google.firebase.analytics/eventTypes/event.log  Yes                 firebase analytics  No
google.firebase.database.ref     providers/google.firebase.database/eventTypes/ref.create  Yes                 firebase database   No
google.firebase.database.ref     providers/google.firebase.database/eventTypes/ref.delete  No                  firebase database   No
google.firebase.database.ref     providers/google.firebase.database/eventTypes/ref.update  No                  firebase database   No
google.firebase.database.ref     providers/google.firebase.database/eventTypes/ref.write   No                  firebase database   No
google.firestore.document        providers/cloud.firestore/eventTypes/document.create      Yes                 firestore document  No
google.firestore.document        providers/cloud.firestore/eventTypes/document.delete      No                  firestore document  No
google.firestore.document        providers/cloud.firestore/eventTypes/document.update      No                  firestore document  No
google.firestore.document        providers/cloud.firestore/eventTypes/document.write       No                  firestore document  No
```



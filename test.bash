last_merge_commit_sha=$(git log --merges -1 --pretty=format:"%H")
if [[ $last_merge_commit_sha == aabd574daa688ca762ee30048ae4a570ec0cc04b ]]; then
  exit 0
else
  exit 1
fi

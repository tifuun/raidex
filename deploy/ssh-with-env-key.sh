#/bin/sh
#
# If you set `GIT_SSH_COMMAND` to the path of this script,
# ssh will use the private key file specified
# in the $RAIDEX_PRIVATE_KEY environment variable.
#
# This script should be called from .github/workflows/deploy.yml
# and the $RAIDEX_PRIVATE_KEY variable should be set
# using github secrets to allow raidex to clone private
# repos.

echo "$RAIDEX_PRIVATE_KEY" | head -c 50

TEMP_SSH_KEY_FILE=$(mktemp)
echo "$RAIDEX_PRIVATE_KEY" > $TEMP_SSH_KEY_FILE
chmod 600 $TEMP_SSH_KEY_FILE
ssh -i $TEMP_SSH_KEY_FILE "$@"
rm -f $TEMP_SSH_KEY_FILE


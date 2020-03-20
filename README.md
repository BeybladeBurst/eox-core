# EOX core

Eox-core (A.K.A. Edunext Open eXtensions) is a [django app plugin](https://github.com/edx/edx-platform/tree/master/openedx/core/djangoapps/plugins) for adding multiple APIS for the [edx-platform](https://github.com/edx/edx-platform) to make changing the platform easier on commercial environments, including bulk creation of pre-activated users (e.g. skip sending an activation email) and enrollments.

## Usage

1) Create the oauth client at http://localhost:18000/admin/oauth2/client/add/ , copy the client-id and client-secret.
2) Generate an auth-token using that client-id and client-secret:
```bash
curl -X POST -d "client_id=<YOUR_CLIENT_ID>&client_secret=<YOUR_CLIENT_SECRET>"`
	`"&grant_type=client_credentials" http://localhost:18000/oauth2/access_token/
```
3) Use the token to call the API as you need:
```bash
# User creation API example
curl -X POST --header "Authorization: Bearer <YOUR_AUTH_TOKEN>" -H "Accept: application/json" \
	http://localhost:18000/eox-core/api/v1/user/ --header "Content-Type: application/json" \
	--data '{"username": "jsmith", "email": "jhon@example.com", "password": "qwerty123",
	"fullname": "Jhon Smith"}'
# Enroll api example
curl -X POST --header "Authorization: Bearer <YOUR_AUTH_TOKEN>" -H "Accept: application/json" \
	http://localhost:18000/eox-core/api/v1/enrollment/ --header "Content-Type: application/json" \
	--data '{"course_id": "course-v1:edX+DemoX+Demo_Course", "email": "edx@example.com",
	"mode": "audit", "force": 1}'
```

## Installation
- Create an edx hawthorn instace if it doesn't exist already:
```bash
# Assuming ubuntu (if not replace apt-get for the package manager of your linux dist, e.g. yum)
sudo apt-get install direnv
cd ~/Documents/
mkdir eoxstack
cd eoxstack
git clone git@github.com:edx/devstack.git
cd devstack
git checkout open-release/hawthorn.master
export OPENEDX_RELEASE=hawthorn.master
make dev.checkout
make dev.clone
make dev.provision
echo export OPENEDX_RELEASE=hawthorn.master > .envrc
```
- Clone the git repo:
```bash
cd ~/Documents/eoxstack/src/  # Change path as needed
sudo mkdir edxapp
cd edxapp
git clone git@github.com:eduNEXT/eox-core.git
```
- Install plugin from your server (in this case the devstack docker lms shell):
```bash
cd ~/Documents/eoxstack/devstack  # Change for your devstack path (if you are using devstack)
make lms-shell  # Enter the devstack machine (or server where lms process lives)
sudo su edxapp -s /bin/bash  # if you are using devstack you need to use edxapp user
source /edx/app/edxapp/venvs/edxapp/bin/activate
cd /edx/src/edxapp/eox-core
pip install -e .
```

## Development
To update dependencies you must edit the .in files (not requirements.txt directly) and compile them using pip-tools:

```bash
$ source /path/to/venv/bin/activate
(venv)$ pip install pip-tools
(venv)$ pip-compile
```

## Integrations with third party services

The plugin offers some integrations listed below:

1. **Sentry**: this service allows to track the errors generated on edx-platform. Check more details in https://sentry.io/welcome/. To enable the integration, follow the steps below:

	* Install the plugin with Sentry support (extras_require [sentry])
	* Sign up/in to your sentry account and create a new Django application integration.
	* Get the DSN for your integration. This is an unique identifier for your application.
	* Setup the following configuration values for edx-platform:

		```yaml
		EOX_CORE_SENTRY_INTEGRATION_DSN: <your DSN value>
		```

	By default, **EOX_CORE_SENTRY_INTEGRATION_DSN** setting is None, which disables the sentry integration.

## Course Management automation compilation

We use webpack to bundle the React js application and its dependencies,
in order to compile for dev environment run this command in the root folder:

npm run build-dev

Otherwise, if you want to compile for use in production environment, run this command instead:

npm run build-prod

This command is defined in the package.json file and export two bundles (a build.js and course-management.bundle.css) inside of eox_core/static folder.

## EOX core migration notes

**Migrating to version 2.0.0**

From version **2.0.0**, middlewares **RedirectionsMiddleware** and **PathRedirectionMiddleware** are now included in this plugin. These middlewares were moved from the **eox-tenant** plugin [here](https://github.com/eduNEXT/eox-tenant/).

if you installed **eox-core** alongside **eox-tenant** plugin, follow the steps below:

- Upgrade eox-tenant to version **1.0.0** (previous releases are not compatible with eox-core 2.0.0)
- Run the plugin migrations as indicated below:
```
   $ python manage.py lms migrate eox_tenant --settings=<your app settings>
   $ python manage.py lms migrate eox_core --fake-initial --settings=<your app settings>
```

In the case eox-tenant is not installed in the platform, just run the eox-core migrations normally.

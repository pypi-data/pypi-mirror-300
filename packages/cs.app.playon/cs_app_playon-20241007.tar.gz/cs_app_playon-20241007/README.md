PlayOn facilities, primarily access to the download API.
Includes a nice command line tool.

*Latest release 20241007*:
Make things more cancellable.

## <a name="main"></a>`main(argv=None)`

Playon command line mode;
see the `PlayOnCommand` class below.

## <a name="PlayOnAPI"></a>Class `PlayOnAPI(cs.service_api.HTTPServiceAPI)`

Access to the PlayOn API.

*`PlayOnAPI.__getitem__(self, download_id: int)`*:
Return the recording `TagSet` associated with the recording `download_id`.

*`PlayOnAPI.account(self)`*:
Return account information.

*`PlayOnAPI.as_contextmanager(self)`*:
Run the generator from the `cls` class specific `__enter_exit__`
method via `self` as a context manager.

Example from `RunState` which subclasses `HasThreadState`,
both of which are `ContextManagerMixin` subclasses:

    class RunState(HasThreadState):
        .....
        def __enter_exit__(self):
            with HasThreadState.as_contextmanager(self):
                ... RunState context manager stuff ...

This runs the `HasThreadState` context manager
around the main `RunState` context manager.

*`PlayOnAPI.auth_token`*:
An auth token obtained from the login state.

*`PlayOnAPI.available(self)`*:
Return the `TagSet` instances for the available recordings.

*`PlayOnAPI.cdsurl_data(self, suburl, _method='GET', headers=None, **kw)`*:
Wrapper for `suburl_data` using `CDS_BASE` as the base URL.

*`PlayOnAPI.download(self, download_id: int, filename=None, *, runstate: Optional[cs.resources.RunState] = <function uses_runstate.<locals>.<lambda> at 0x10becfce0>)`*:
Download the file with `download_id` to `filename_basis`.
Return the `TagSet` for the recording.

The default `filename` is the basename of the filename
from the download.
If the filename is supplied with a trailing dot (`'.'`)
then the file extension will be taken from the filename
of the download URL.

*`PlayOnAPI.feature(self, feature_id)`*:
Return the feature `SQLTags` instance for `feature_id`.

*`PlayOnAPI.featured_image_url(self, feature_name: str)`*:
URL of the image for a featured show.

*`PlayOnAPI.features(self)`*:
Fetch the list of featured shows.

*`PlayOnAPI.from_playon_date(date_s)`*:
The PlayOn API seems to use UTC date strings.

*`PlayOnAPI.jwt`*:
The JWT token.

*`PlayOnAPI.login(self)`*:
Perform a login, return the resulting `dict`.
*Does not* update the state of `self`.

*`PlayOnAPI.login_expiry`*:
Expiry UNIX time for the login state.

*`PlayOnAPI.notifications(self)`*:
Return the notifications.

*`PlayOnAPI.queue(self)`*:
Return the `TagSet` instances for the queued recordings.

*`PlayOnAPI.recordings(self)`*:
Return the `TagSet` instances for the available recordings.

*`PlayOnAPI.renew_jwt(self)`*:
UNUSED

*`PlayOnAPI.service(self, service_id: str)`*:
Return the service `SQLTags` instance for `service_id`.

*`PlayOnAPI.services(self)`*:
Fetch the list of services.

*`PlayOnAPI.suburl(self, suburl, *, api_version=None, headers=None, _base_url=None, **kw)`*:
Override `HTTPServiceAPI.suburl` with default
`headers={'Authorization':self.jwt}`.

*`PlayOnAPI.suburl_data(self, suburl, *, raw=False, **kw)`*:
Call `suburl` and return the `'data'` component on success.

Parameters:
* `suburl`: the API subURL designating the endpoint.
* `raw`: if true, return the whole decoded JSON result;
  the default is `False`, returning `'success'` in the
  result keys and returning `result['data']`
Other keyword arguments are passed to the `HTTPServiceAPI.json` method.

## <a name="PlayOnCommand"></a>Class `PlayOnCommand(cs.cmdutils.BaseCommand)`

Playon command line implementation.

Usage summary:

    Usage: playon subcommand [args...]

        Environment:
          PLAYON_USER               PlayOn login name, default from $EMAIL.
          PLAYON_PASSWORD           PlayOn password.
                                    This is obtained from .netrc if omitted.
          PLAYON_FILENAME_FORMAT  Format string for downloaded filenames.
                                    Default: {series_prefix}{series_episode_name}--{resolution}--{playon.ProviderID}--playon--{playon.ID}
          PLAYON_TAGS_DBURL         Location of state tags database.
                                    Default: ~/var/playon.sqlite

        Recording specification:
          an int        The specific recording id.
          all           All known recordings.
          downloaded    Recordings already downloaded.
          expired       Recording which are no longer available.
          pending       Recordings not already downloaded.
          /regexp       Recordings whose Series or Name match the regexp,
                        case insensitive.
      
      Subcommands:
        account
          Report account state.
        api suburl
          GET suburl via the API, print result.
        cds suburl
          GET suburl via the content delivery API, print result.
          Example subpaths:
            content
            content/provider-name
        dl [-j jobs] [-n] [recordings...]
          Download the specified recordings, default "pending".
          -j jobs   Run this many downloads in parallel.
                    The default is 2.
          -n        No download. List the specified recordings.
        downloaded recordings...
          Mark the specified recordings as downloaded and no longer pending.
        feature [feature_id]
          List features.
        help [-l] [subcommand-names...]
          Print help for subcommands.
          This outputs the full help for the named subcommands,
          or the short help for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        ls [-l] [recordings...]
          List available downloads.
          -l        Long listing: list tags below each entry.
          -o format Format string for each entry.
          Default format: {playon.ID} {playon.HumanSize} {resolution} {nice_name} {playon.ProviderID} {status:upper}
        poll [options...]
        q [-l] [recordings...]
          List queued recordings.
          -l        Long listing: list tags below each entry.
          -o format Format string for each entry.
          Default format: {playon.ID} {playon.Series} {playon.Name} {playon.ProviderID}
        queue [-l] [recordings...]
          List queued recordings.
          -l        Long listing: list tags below each entry.
          -o format Format string for each entry.
          Default format: {playon.ID} {playon.Series} {playon.Name} {playon.ProviderID}
        refresh [queue] [recordings]
          Update the db state from the PlayOn service.
        rename [-o filename_format] filenames...
          Rename the filenames according to their fstags.
          -n    No action, dry run.
          -o filename_format
                Format for the new filename, default '{series_prefix}{series_episode_name}--{resolution}--{playon.ProviderID}--playon--{playon.ID}'.
        service [service_id]
          List services.
        shell
          Run a command prompt via cmd.Cmd using this command's subcommands.

*`PlayOnCommand.Options`*

*`PlayOnCommand.cmd_account(self, argv)`*:
Usage: {cmd}
Report account state.

*`PlayOnCommand.cmd_api(self, argv)`*:
Usage: {cmd} suburl
GET suburl via the API, print result.

*`PlayOnCommand.cmd_cds(self, argv)`*:
Usage: {cmd} suburl
GET suburl via the content delivery API, print result.
Example subpaths:
  content
  content/provider-name

*`PlayOnCommand.cmd_dl(self, argv)`*:
Usage: {cmd} [-j jobs] [-n] [recordings...]
Download the specified recordings, default "pending".
-j jobs   Run this many downloads in parallel.
          The default is {DEFAULT_DL_PARALLELISM}.
-n        No download. List the specified recordings.

*`PlayOnCommand.cmd_downloaded(self, argv, locale='en_US')`*:
Usage: {cmd} recordings...
Mark the specified recordings as downloaded and no longer pending.

*`PlayOnCommand.cmd_feature(self, argv, locale='en_US')`*:
Usage: {cmd} [feature_id]
List features.

*`PlayOnCommand.cmd_ls(self, argv)`*:
Usage: {cmd} [-l] [recordings...]
List available downloads.
-l        Long listing: list tags below each entry.
-o format Format string for each entry.
Default format: {LS_FORMAT}

*`PlayOnCommand.cmd_q(self, argv)`*:
Usage: {cmd} [-l] [recordings...]
List queued recordings.
-l        Long listing: list tags below each entry.
-o format Format string for each entry.
Default format: {QUEUE_FORMAT}

*`PlayOnCommand.cmd_queue(self, argv)`*:
Usage: {cmd} [-l] [recordings...]
List queued recordings.
-l        Long listing: list tags below each entry.
-o format Format string for each entry.
Default format: {QUEUE_FORMAT}

*`PlayOnCommand.cmd_refresh(self, argv)`*:
Usage: {cmd} [queue] [recordings]
Update the db state from the PlayOn service.

*`PlayOnCommand.cmd_rename(self, argv, *, fstags: Optional[cs.fstags.FSTags] = <function <lambda> at 0x10a443060>)`*:
Usage: {cmd} [-o filename_format] filenames...
Rename the filenames according to their fstags.
-n    No action, dry run.
-o filename_format
      Format for the new filename, default {DEFAULT_FILENAME_FORMAT!r}.

*`PlayOnCommand.cmd_service(self, argv, locale='en_US')`*:
Usage: {cmd} [service_id]
List services.

*`PlayOnCommand.run_context(self)`*:
Prepare the `PlayOnAPI` around each command invocation.

## <a name="PlayonSeriesEpisodeInfo"></a>Class `PlayonSeriesEpisodeInfo(cs.mediainfo.SeriesEpisodeInfo)`

A `SeriesEpisodeInfo` with a `from_Recording()` factory method to build 
one from a PlayOn `Recording` instead or other mapping with `playon.*` keys.

*`PlayonSeriesEpisodeInfo.from_Recording(R: Mapping[str, Any])`*:
Infer series episode information from a `Recording`
or any mapping with ".playon.*" keys.

## <a name="PlayOnSQLTags"></a>Class `PlayOnSQLTags(cs.sqltags.SQLTags)`

`SQLTags` subclass with PlayOn related methods.

*`PlayOnSQLTags.__getitem__(self, index)`*:
Override `SQLTags.__getitem__` to promote `int` indices
to a `str` with value `f'recording.{index}'`.

*`PlayOnSQLTags.__iter__(self)`*:
Yield recording `TagSet`s, those named `"recording.*"`.

Note that this includes both recorded and queued items.

*`PlayOnSQLTags.infer_db_url(envvar=None, default_path=None)`*:
Infer the database URL.

Parameters:
* `envvar`: environment variable to specify a default,
  default from `DBURL_ENVVAR` (`PLAYON_TAGS_DBURL`).

*`PlayOnSQLTags.recording_ids_from_str(self, arg)`*:
Convert a string to a list of recording ids.

*`PlayOnSQLTags.recordings(self)`*:
Yield recording `TagSet`s, those named `"recording.*"`.

Note that this includes both recorded and queued items.

## <a name="Recording"></a>Class `Recording(cs.sqltags.SQLTagSet)`

An `SQLTagSet` with knowledge about PlayOn recordings.

*`Recording.filename(self, filename_format=None) -> str`*:
Return the computed filename per `filename_format`,
default from `DEFAULT_FILENAME_FORMAT`: `'{series_prefix}{series_episode_name}--{resolution}--{playon.ProviderID}--playon--{playon.ID}'`.

*`Recording.is_available(self)`*:
Is a recording available for download?

*`Recording.is_downloaded(self)`*:
Test whether this recording has been downloaded
based on the presence of a `download_path` `Tag`
or a true `downloaded` `Tag`.

*`Recording.is_expired(self)`*:
Test whether this recording is expired,
which implies that it is no longer available for download.

*`Recording.is_pending(self)`*:
A pending download: available and not already downloaded.

*`Recording.is_queued(self)`*:
Is a recording still in the queue?

*`Recording.is_stale(self, max_age=None)`*:
Override for `TagSet.is_stale()` which considers expired
records not stale because they can never be refrehed from the
service.

*`Recording.ls(self, ls_format=None, long_mode=False, print_func=None)`*:
List a recording.

*`Recording.nice_name(self)`*:
A nice name for the recording: the PlayOn series and name,
omitting the series if `None`.

*`Recording.recording_id(self)`*:
The recording id or `None`.

*`Recording.resolution(self)`*:
The recording resolution derived from the quality
via the `Recording.RECORDING_QUALITY` mapping.

*`Recording.series_prefix(self)`*:
Return a series prefix for recording containing the series name
and season and episode, or `''`.

*`Recording.status(self)`*:
Return a short status string.

# Release Log



*Release 20241007*:
Make things more cancellable.

*Release 20240723*:
* Replace many raises of RuntimeError with NotImplementedError, suggestion by @dimaqq on discuss.python.org.
* This update tracks some bugfixes in some required modules.

*Release 20240522*:
New superior tv-series/season/episode inference.

*Release 20240316*:
Fixed release upload artifacts.

*Release 20240201.1*:
Release with "playon" script.

*Release 20240201*:
* PlayOnCommand.cmd_dl: collapse dashes more reliably, restore the space squashing, make the downloads interruptable.
* PlayOnCommand._list: sort each listing argument by recording id.

*Release 20230705*:
DEFAULT_FILENAME_FORMAT: replace naive playon.Name with series_episode_name which is the name with leading series/episode info removed, honour in "playon dl".

*Release 20230703*:
* PlayOnAPI: features, feature, featured_image_url, service_image_url.
* PlayOnCommand: new cmd_feature like cmd_service but for featured shows.
* PlayOnAPI.suburl: infer _base_url from api_version if _base_url is None and api_version is provided.
* Recording.is_downloaded: also check for a 'downloaded' tag, fallback for when the downloaded_path is empty.
* PlayOnCommand.cmd_downloaded: add 'downloaded" tag to specified recordings.

*Release 20230217*:
* Move some core stuff off into cs.service_api.HTTPServiceAPI.
* Move core Recording.is_stale() method to TagSet.is_stale(), leave override method behind.
* Persist login tokens in a db for reuse while still fresh.
* "playon dl": allow interrupting downloads.
* Cleaner handling of playon.Name having a leading SNNeNN prefix.

*Release 20221228*:
* PlayOnAPI.suburl_data: progress reporting, raise on bad response, upgrade JSON error warning.
* PlayOnAPI: use a common cookie jar across API calls.
* PlayOnCommand: new "api" and "cds" API access subcommands.
* PlayOnCommand._refresh_sqltags_data: bugfix "expired cache" logic.
* PlayOnCommand: new "poll" subcommand reporting the API notifications response.

*Release 20220311*:
Bugfix criteria for refreshing the PlayOn state.

*Release 20211212*:
Initial release.

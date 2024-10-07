.. include:: /includes/_links.rst

Upgrade to 6.x Releases
=======================

.. toctree::
   :maxdepth: 2

This article provides information on how to upgrade to the latest 6.x
releases from old releases such as 4.x and 5.x.

Issues in 4.x Releases
----------------------

The old releases were finished before 2020 by Ilya Etingof and wasn't well
maintained after 2019. While Ilya kept the project alive, the project was
not living up to its potential nor following the best practices of the
modern software development,

#. Many legacy code existed to keep compatibility with very old Python
   versions like 2.x. That added unnecessary complexity to the project and
   made it hard to maintain and develop new features.
#. The core library was not well covered by simple unit test cases. So when
   certain features were added or patched, and listed in release notes, not
   enough information is available on why the changes were needed. And even
   if we wanted to clean up or refactor the code, we couldn't do it easily
   without breaking the existing functionality. Later we found out that
   more test cases were on unstable branches, but they were more like
   end to end tests rather than unit tests and you couldn't run them easily
   with debuggers.

Ilya wasn't able to produce the 4.4.13 release, so the last stable release
from him was 4.4.12.

.. note::

   We were able to cherry pick the changes on 4.4.13 branch and merge them
   into the 6.1 release.

.. warning::

   You can see there are tons of known issues with 4.x releases, and they
   also work badly with the latest Python versions, so please don't stay
   with them for long.

Issues in 5.x Releases
----------------------

While working on 4.x releases, Ilya actually kept a master branch with some
experimental changes and planned to release as 5.0. However, this plan
wasn't finished and irrelevant to what you see today the 5.x releases from
other maintainers and their forks.

.. note::

   We called Ilya's changes experimental because they were not well tested
   and when we used our test suite to thoroughly play with the changes, we
   found out that some of them were poorly designed and not really working
   as expected.

   For example, the revised MIB implementation used hard-to-understand
   callbacks everywhere and deep recursion, which might work if you have
   only simple operations to execute. But when you have to deal with some
   real-world scenarios, the recursion depth was easily reached and the
   whole operation was failed.

   We are still evaluating all the changes Ilya made and will decide
   whether to keep them or not in the future releases.

It took the Splunk team and LeXtudio team each several months to get
familiar with the code base and they chose different ways to advance the
project.

In short, the following were done by the Splunk team,

* The build system was migrated to poetry, which is a modern Python
  packaging tool that simplifies the process of packaging and distributing
  Python packages. Testing the bits on Python 3.8-3.12 couldn't be easier.
* Legacy code for Python 2.x was removed, while many changes required by
  newer Python versions (3.8 to 3.11) was applied.
* Some patches created by the community between 2019 and 2022 were merged
  into the code base.
* Testing started to become a top priority, but mainly through integration
  tests with Splunk components.
* The API surface was kept compatible with the 4.x releases in most cases.

From there, the Splunk team built its own 5.0.x releases from Ilya's 4.4.12
branch.

This was then followed by the LeXtudio team, but they added more changes to
the code base,

* New changes required by Python 3.12 were applied, such as completely free
  of asyncore.
* A relatively complete unit test suite was added to the code base, so that
  from there bugfixes and refactoring could be done with confidence.
* Many more community patches were tested and merged.
* Collaboration with downstream projects like OpenStack and Home Assistant
  was started so that compatibility with their projects could be reviewed
  and improved.
* Documentation was updated to reflect the changes.

.. warning::

   We consider the 5.0.x release as a stepping stone to the 6.x releases,
   so please don't stay with them for long.

Upgrade to 6.x Releases
-----------------------

The 6.0 release is the first major release upgrade by LeXtudio Inc., after
the team took over the project and attempted twice internally to modernize
the code base. So far, this release introduces the following changes:

* Unit test coverage is further improved.
* Legacy API based on asyncore has been completely removed.
* New sync API based on asyncio is added to enable synchronous I/O
  operations and easy migration from 4.x/5.0 releases.
* The API surface was adjusted slightly to make it more aligned with other
  SNMP implementations.
* Documentation is significantly improved to cover the new features and
  changes.
* Continuous collaboration with downstream projects.

PySMI 1.3 and 1.4 releases introduced some changes that are not fully
compatible with PySMI 1.2. So we decided to keep PySNMP 6.0 with PySMI 1.2,
and release PySNMP 6.1 release to support users who prefer PySMI 1.3 and
above. As the quality of asyncio-based sync API is not as good as we expect,
we decided to remove it from 6.2 release.

Important Changes
-----------------

The following changes are important to note when upgrading to 6.x:

Async API based on asyncore
+++++++++++++++++++++++++++

All such APIs are removed, so you can no longer import types from the
relevant modules. This includes the old sync API (based on asyncore).

Sync API based on asyncio
+++++++++++++++++++++++++

The new sync API is added to enable synchronous I/O operations and easy
migration from 4.x/5.x releases. The new API is based on asyncio and is
compatible with Python 3.8 and later.

We were hoping the new sync API would be stable enough to meet the quality
expectation, but it turned out to be the opposite. So we decided to remove it
from 6.2 release.

RFC3414 Compliance
++++++++++++++++++

The engine request/response processing wasn't fully compliant with RFC3414,
especially when it came to error handling.

Initial changes were introduced to better support time synchronization in
5.0 release, but more changes are included in 6.0 release to make the
engine fully compliant with RFC3414.

Related Resources
-----------------

- `Support Options`_
- :doc:`/troubleshooting`
- :doc:`/examples/index`
- :doc:`/docs/api-reference`

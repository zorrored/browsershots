# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Database interface for screenshot table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

def select_recent(website, limit=5):
    """
    Get the most recently uploaded screenshots for a website.
    """
    cur.execute("""\
SELECT hashkey FROM screenshot
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
WHERE website = %s
ORDER BY screenshot.created DESC
LIMIT %s
""", (website, limit))
    return cur.fetchall()

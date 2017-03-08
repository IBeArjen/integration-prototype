# -*- coding: utf-8 -*-
""" Test of docker platform as a service

.. moduleauthor:; David Terrett <david.terrett@stfc.ac.uk>
"""

import rpyc
import time
import unittest
import warnings

from sip_common.docker_paas import DockerPaas as Paas
from sip_common.paas import TaskStatus

class TestDocker(unittest.TestCase):

    # dockerpy keeps the socket to the docker engine open so we need to
    # suppress the resource warning from unittest
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)

    def testTask(self):
        """ Test normal execution of task
        """
        s = Paas()

        # Start the task
        t = s.run_task('test_task', 'test_image', 
                ['python3', '/home/sdp/test_task.py', '3', '0'])
    
        # It should be running
        self.assertEqual(t.status(), TaskStatus.RUNNING)

        # Wait for it to end and it should be ended
        time.sleep(5)
        #self.assertEqual(t.status(), TaskStatus.EXITED)

        # Stop the task 
        t.delete()

    def testService(self):
        """ Test normal execution of service
        """
        s = Paas()

        # Start the task
        t = s.run_service('test_service', 'test_image', 9999,
                ['python3', '/home/sdp/test_service.py', '9999'])
    
        # It should be running
        self.assertEqual(t.status(), TaskStatus.RUNNING)

        # Wait 10 seconds for it to start (yes really!)
        time.sleep(10)

        # Check that we can talk to it
        (hostname, port) = t.location()
        conn = rpyc.connect(host=hostname, port=port)
        conn.root.hello()

        # Stop the task 
        t.delete()

    def xtestStop(self):
        """ Test of stopping a task
        """
        s = Paas()
        t = s.run_task('test_stop', 'python3', 
                ['python3', '/home/spd/test_task.py', '3', '0'])
        time.sleep(1)
    
        self.assertEqual(t.status(), TaskStatus.RUNNING)
        t.delete()
        self.assertEqual(t.status(), TaskStatus.EXITED)

    def xtestEndInError(self):
        """ Test of task that exits with an error status
        """
        s = Paas()
        t = s.run_task('test', 'python3', ['python3', 'test_task.py', '0', '1'])
        time.sleep(1)
        self.assertEqual(t.status(), TaskStatus.ERROR)
        t.delete()
    
    def testDuplicateService(self):
        """ Test trying to start a service twice with the same name
        """
        s = Paas()

        # Start the task
        t1 = s.run_service('test_dup', 'python3', 9999,
                ['python3', 'test_service.py', '9999'])

        t2 = s.run_service('test_dup', 'python3', 9999,
                    ['python3', 'test_service.py', '9999'])

        self.assertEqual(t1.ident, t2.ident)

        t1.delete()
    
    def testDuplicateTask(self):
        """ Test trying to start a task twice with the same name
        """
        s = Paas()

        # Start the task
        t1 = s.run_task('test_dup', 'python3', 
                ['python3', 'test_task.py', '0', '0'])

        # Try another
        t2 = s.run_task('test_dup', 'python3', 
                    ['python3', 'test_task.py', '0', '0'])

        self.assertNotEqual(t1.ident, t2.ident)
        t2.delete()

    def testFind(self):
        """ Test finding a task
        """
        s = Paas()

        # Start the task
        t1 = s.run_task('test_find', 'python3', 
                ['python3', 'test_task.py', '0', '0'])

        # Find it
        t2 = s.find_task('test_find')

        self.assertEqual(t1.ident, t2.ident)
        t2.delete()
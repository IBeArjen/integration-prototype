# -*- coding: utf-8 -*-
"""Module to stream SPEAD visibility data.

The visibility data is sent as a number of SPEAD heaps, with a have a structure
(payload) defined in the CSP-SDP ICD documents. Heaps are sent to a stream
which is a UDP socket.
"""
import spead2
import spead2.send
import numpy as np
import time
from logging import Logger
# import spead2.send.asyncio
# import asyncio


class HeapStreamer:
    """Class for sending SPEAD heaps to one or more SPEAD streams (UDP sockets).

    Streams are configured according to a python dictionary passed to the
    constructor. The content of the data sent in each heap (the payload)
    is defined in the relevant CSP-SDP ICD documents.

    Usage example::

        config = dict(sender_node=[])
        frame_shape = (1, 1, 1, 435, 4)
        streamer = HeapStreamer(config, frame_shape)
        streamer.start()
        for i in range(num_heaps):
            streamer.payload['timestamp_utc'] = [(i, 0)]
            streamer.payload['complex_visibility'] = get_vis_data(i)
            streamer.send_heap(i)
        streamer.end()

    Configuration::

        {
            "sender_node": {
                "streams": [
                    {
                        "port": 8001,
                        "host": "127.0.0.1"
                        "threads": 1
                    }
                ]
            }
        }

    - ``streams`` is a list of dictionaries of describing where SPEAD heap data
      should be sent.
    - Each stream dictionary can have the keys: ``port``, ``host``, and
      ``threads``.
    - ``port`` and ``host`` are required keys and give the address to which
      SPEAD heaps should be sent.
    - ``threads`` is optional (default: 1) and sets the number of threads used
      in sending the heap.
    """

    # FIXME(BM) do not pass logger object to this method!
    def __init__(self, config, frame_shape, num_pol, log=Logger(__name__)):
        """Creates and sets up SPEAD streams.

        The configuration of streams is passed in via the ``config`` arguent.

        The dimensions of the visibility data must be specified in order
        to initialise the payload. This is a tuple of dimensions defined in the
        ICD as:


        Args:
            config (dict): Dictionary of settings (see above).
            frame_shape (tuple): Dimensions of the payload visibility data.
            log (logging.Logger): Python logging object.
        """
        self._config = config
        self._frame_shape = frame_shape
        self._num_pol = num_pol
        self._log = log
        self._heap_descriptor = self._init_heap_descriptor()
        self._streams = list()
        self._heap_counter = 0
        self._send_timer = 0
        self._heap_size = self._get_heap_size()
        self._create_streams()
        self._payload = self._init_payload()

    def start(self):
        """Send the start of stream message to each stream."""
        self._heap_counter = 0
        self._send_timer = 0
        for stream, item_group in self._streams:
            # Blocking send
            stream.send_heap(item_group.get_start())
            
            # Async Send
            # stream.async_send_heap(item_group.get_start())
            # asyncio.async(stream.async_send_heap(item_group.get_start()))

    def end(self):
        """Send the end of stream message to each stream."""
        for stream, item_group in self._streams:
            # Blocking send
            stream.send_heap(item_group.get_end())
            
            # Async Send
            # stream.async_send_heap(item_group.get_end())
            # asyncio.async(stream.async_send_heap(item_group.get_end()))

    def send_heap(self, heap_index, stream_id=0):
        """Send one heap with the data contained in self.payload to the
        specified stream ID.

        Args:
            heap_index (int): HEAP index.
            stream_id (int): Stream index (default=0).
        """
        self._log.debug('  heap_descriptor {:03d}'.format(heap_index))
        # Update the values of items in the item group for this stream.
        t0 = time.time()
        stream, item_group = self._streams[stream_id]
        for name, item in item_group.items():
            self._log.debug('    item: 0x{:04X} {}'.format(item.id, name))

            item.value = self._payload[name]

        # Send the updated heap_descriptor
        _heap = item_group.get_heap()
        # Blocking Send
        stream.send_heap(_heap)
        
        # Async Send
        # futures = [
        #     asyncio.async(stream.async_send_heap(_heap))
        # ]
        # Async Send
        # asyncio.get_event_loop().run_until_complete(asyncio.wait(futures))

        self._heap_counter += 1
        self._send_timer += (time.time() - t0)

    @property
    def payload(self):
        """Payload attribute.

        This is a dictionary containing the payload for the HEAP.
        This dictionary should be modified before calling send_heap() to
        update the data sent.

        Payload has the following keys

        * timestamp_utc
        * channel_baseline_id
        * channel_baseline_count
        * schedule_block
        * hardware_source_id
        * complex_visibility
        * time_centroid_index
        * flagging_fraction
        """
        return self._payload

    @payload.setter
    def payload(self, **kwargs):
        print(kwargs)

    @payload.deleter
    def payload(self):
        del self._payload



    def _get_heap_size(self):
        """Return the total size of items in the SPEAD heap in bytes."""
        heap_size = 0
        for item in self._heap_descriptor:
            num_elements = np.prod(item['shape'])
            if 'type' in item:
                heap_size += np.dtype(item['type']).itemsize * num_elements
            elif 'format' in item:
                item_bits = sum(bits for _, bits in item['format'])
                heap_size += item_bits // 8 * num_elements
        return heap_size

    @staticmethod
    def _get_config_r(settings, key, default=None):
        """Read a configuration value from a settings dictionary

        FIXME(BM) Just use dict get() method instead?
        https://docs.python.org/3.6/library/stdtypes.html#dict.get
        """
        value = default
        if len(key) == 1:
            if key[0] in settings:
                value = settings[key[0]]
        else:
            if key[0] in settings:
                return HeapStreamer._get_config_r(settings[key[0]], key[1:],
                                                  default)
        return value

    def _get_config(self, key, default=None):
        """Read a configuration value"""
        return self._get_config_r(self._config, key, default)

    def _create_streams(self):
        """Construct streams, item group and item descriptions."""
        # Construct the SPEAD flavour description
        parent = 'spead_flavour'
        version = self._get_config([parent, 'version'], 4)
        item_pointer_bits = self._get_config([parent, 'item_pointer_bits'], 64)
        heap_address_bits = self._get_config([parent, 'heap_address_bits'], 40)
        bug_compat_mask = self._get_config([parent, 'bug_compat_mask'], 0)
        flavour = spead2.Flavour(version, item_pointer_bits, heap_address_bits,
                                 bug_compat_mask)

        # Construct UDP stream objects and associated heap_descriptor item
        # groups.
        streams = list()
        for i, stream in enumerate(self._config['sender_node']['streams']):
            host = stream['host']
            port = stream['port']
            threads = stream['threads'] if 'threads' in stream else 1
            stream_config = spead2.send.StreamConfig(rate=0)
            thread_pool = spead2.ThreadPool(threads=threads)
            # Blocking send
            stream = spead2.send.UdpStream(thread_pool, host, port,
                                           stream_config)

            # Asynchronous Send
            # stream = spead2.send.asyncio.UdpStream(thread_pool, host, port,
            #                                         stream_config)

            item_group = spead2.send.ItemGroup(flavour=flavour)
            # Append stream & item group the stream list.
            streams.append((stream, item_group))

            self._log.debug('Configuring stream {}:'.format(i))
            self._log.debug('  Address = {}:{}'.format(host, port))
            self._log.debug('  Flavour = SPEAD-{}-{} v{} compat:{}'.
                            format(flavour.item_pointer_bits,
                                  flavour.heap_address_bits,
                                  flavour.version,
                                  flavour.bug_compat))
            self._log.debug('  Threads = {}'.format(threads))


            # Add items to the item group based on the heap_descriptor
            for j, item in enumerate(self._heap_descriptor):
                item_id = item['id']
                if isinstance(item_id, str):
                    item_id = int(item_id, 0)
                name = item['name']
                desc = item['description']
                item_type = item['type'] if 'type' in item else None
                item_format = item['format'] if 'format' in item else None
                # if 'shape' not in item:
                #     raise RuntimeError('shape not defined for {}'.format(name))
                shape = item['shape']
                item_group.add_item(item_id, name, desc, shape=shape,
                                    dtype=item_type, format=item_format)
                self._log.debug('Adding item {} : {} {}'.format(j, item_id,
                                                                name))
                self._log.debug('  description = {}'.format(desc))
                if item_type is not None:
                    self._log.debug('  type = {}'.format(item_type))
                if item_format is not None:
                    self._log.debug('  format = {}'.format(item_format))
                    self._log.debug('  shape = {}'.format(shape))

        self._streams = streams


    def _init_heap_descriptor(self):
        """Return the heap descriptor dictionary."""
        heap_descriptor = [
            # Per SPEAD heap_descriptor
            {
                "id": 0x8000,
                "name": "visibility_timestamp_count",
                "description": "SDP_REQ_INT-45.",
                "format": [('u', 32)],
                "shape": (1,)
            },
            {
                "id": 0x8001,
                "name": "visibility_timestamp_fraction",
                "description": "SDP_REQ_INT-45.",
                "format": [('u', 32)],
                "shape": (1,)
            },
            {
                "id": 0x8002,
                "name": "visibility_channel_id",
                "description": "",
                "format": [('u', 32)],
                "shape": (1,)
            },
            {
                "id": 0x8003,
                "name": "visibility_channel_count",
                "description": "SDP_REQ_INT-47",
                "format": [('u', 32)],
                "shape": (1,)
            },
            {
                "id": 0x8004,
                "name": "visibility_baseline_polarisation_id",
                "description": "SDP_REQ_INT-46",
                "format": [('u', 32)],
                "shape": (1,)
            },
            {
                "id": 0x8005,
                "name": "visibility_baseline_count",
                "description": "SDP_REQ_INT-47",
                "format": [('u', 32)],
                "shape": (1,)
            },
            {
                "id": 0x8006,
                "name": "phase_bin_id",
                "description": "",
                "format": [('u', 16)],
                "shape": (1,)
            },
            {
                "id": 0x8007,
                "name": "phase_bin_count",
                "description": "",
                "format": [('u', 16)],
                "shape": (1,)
            },
            {
                "id": 0x8008,
                "name": "schedule_block_id",
                "description": "SDP_REQ_INT-48",
                "format": [('u', 48)],
                "shape": (1,)
            },
            {
                "id": 0x8009,
                "name": "visibility_hardware_id",
                "description": "SDP_REQ_INT-49",
                "format": [('u', 32)],
                "shape": (1,)
            },
            {
                "id": 0x800D,
                "name": "correlator_output_data",
                "description": "",
                "type": [('TCI', 'i8'), ('FD', 'u8'), ('VIS', 'c8', self._num_pol)],
                "shape": self._frame_shape
            }
        ]
        return heap_descriptor

    def _init_payload(self):
        """Return an empty payload"""
        payload = dict(
            visibility_timestamp_count=[0],
            visibility_timestamp_fraction=[0],
            visibility_channel_id=[0],
            visibility_channel_count=[0],
            visibility_baseline_polarisation_id=[0],
            visibility_baseline_count=[0],
            phase_bin_id=[0],
            phase_bin_count=[0],
            schedule_block_id=[0],
            visibility_hardware_id=[0],
            correlator_output_data=np.zeros(
                (self._frame_shape),dtype=[('TCI', 'i8'), ('FD', 'u8'), ('VIS', 'c8', self._num_pol)])
        )
        return payload
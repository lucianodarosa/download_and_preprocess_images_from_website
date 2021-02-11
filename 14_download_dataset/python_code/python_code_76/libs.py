import tensorflow as tf
import os
import glob
import configparser
import cv2
import mysql.connector

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)

slash = '/'


def mysql_connect(_dbname):

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='paho3047@',
        database=_dbname
    )
    return mydb


def bin_search_range(_array, _value):

    def first_pos(_array, _value, _low: int, _high: int):
        _id = -1
        while _low <= _high:
            _mid = int(_low + (_high - _low) / 2)
            if _array[_mid] >= _value:
                _id = _mid
                _high = _mid - 1
            else:
                _low = _mid + 1
        return _id

    def last_pos(_array, _value, _low: int, _high: int):
        _id = -1
        while _low <= _high:
            _mid = int(_low + (_high - _low) / 2)
            if _array[_mid] <= _value:
                _id = _mid
                _low = _mid + 1
            else:
                _high = _mid - 1
        return _id

    _low = first_pos(_array, _value, 0, len(_array) - 1)
    _high = last_pos(_array, _value, 0, len(_array) - 1)

    if _low != _high:
        return _low, _high
    else:
        return -1, -1


def bin_search(_array, _value, _left: int, _right: int):

    while _left <= _right:

        _middle = int(_left + (_right - _left) / 2)

        if _array[_middle] == _value:
            return _middle

        elif _array[_middle] < _value:
            _left = _middle + 1

        else:
            _right = _middle - 1

    return -1


# set bar into end of string path file
def setbar(_path: str):

    # if last character is not a bar
    if _path[len(_path) - 1:] != '/':
        _path = _path + '/'

    # return path
    return _path


# get number of shards from split based on size of shards
def get_shard_num(_split_size: int, _shard_size: int):

    # get number of shards
    _shard_num = _split_size // _shard_size

    # increase number of shards if rest of division is greater than zero
    if (_split_size % _shard_size) != 0:
        _shard_num += 1

    return _shard_num


# get all images from input path dataset
def get_all_file_paths(_dir, _ext):

    def find_tree_sub_folders(_dir):

        _sub_folders = []
        if os.path.isdir(_dir):

            _sub_folders.append(_dir)

            _folders = os.listdir(_dir)
            _folders.sort()

            for _folder in _folders:
                _sub_dir = _dir + slash + _folder

                if os.path.isdir(_sub_dir):
                    _next_subfolders = find_tree_sub_folders(_sub_dir)

                    _sub_folders = _sub_folders + _next_subfolders

        return _sub_folders

    def find_img_files(_folders, _ext):

        _img_paths = []
        for _folder in _folders:

            _files = os.listdir(_folder)
            _files.sort()

            for _file in _files:
                if _file.endswith(_ext):
                    _img_paths.append(_folder + slash + _file)

        return _img_paths

    return find_img_files(find_tree_sub_folders(_dir), _ext)


def create_dataset_cfg_file(_path_in: str, _path_out: str, _train_split_prct: float, _val_split_prct: float,
                            _test_split_prct: float, _dataset_size: int, _train_split_size: int, _val_split_size: int,
                            _test_split_size: int, _shard_size: int, _shard_train_num: int, _shard_val_num: int,
                            _shard_test_num: int, _img_size: int, _img_depth: int, _folder_name: str):

    path_cfg = _path_out + _folder_name + '/' + _folder_name + '.ini'

    try:
        os.remove(path_cfg)
    except:
        pass

    filecfg = open(path_cfg, 'w')

    # Add content to the file
    Config = configparser.ConfigParser()

    Config.add_section('params')

    Config.set('params', 'path_in', str(_path_in))
    Config.set('params', 'path_out', str(_path_out) + str(_folder_name))
    Config.set('params', 'train_split_prct', str(_train_split_prct))
    Config.set('params', 'val_split_prct', str(_val_split_prct))
    Config.set('params', 'test_split_prct', str(_test_split_prct))
    Config.set('params', 'dataset_size', str(_dataset_size))
    Config.set('params', 'train_split_size', str(_train_split_size))
    Config.set('params', 'val_split_size', str(_val_split_size))
    Config.set('params', 'test_split_size', str(_test_split_size))
    Config.set('params', 'shard_size', str(_shard_size))
    Config.set('params', 'shard_train_num', str(get_shard_num(_train_split_size, _shard_size)))
    Config.set('params', 'shard_val_num', str(get_shard_num(_val_split_size, _shard_size)))
    Config.set('params', 'shard_test_num', str(get_shard_num(_test_split_size, _shard_size)))
    Config.set('params', 'img_size', str(_img_size))
    Config.set('params', 'img_depth', str(_img_depth))

    Config.write(filecfg)

    filecfg.close()


def read_dataset_cfg_file(_dataset_path: str):

    configfile_name = ''
    try:
        # get image files paths in current directory
        configfile_name = glob.glob(_dataset_path + '*.ini')
    except:
        pass

    cfgfile = configparser.ConfigParser()
    cfgfile.read(configfile_name)

    return float(cfgfile['params']['train_split_prct']), float(cfgfile['params']['val_split_prct']), float(
        cfgfile['params']['test_split_prct']), int(cfgfile['params']['dataset_size']), int(
        cfgfile['params']['train_split_size']), int(cfgfile['params']['val_split_size']), int(
        cfgfile['params']['test_split_size']), int(cfgfile['params']['shard_size']), int(
        cfgfile['params']['shard_train_num']), int(cfgfile['params']['shard_val_num']), int(
        cfgfile['params']['shard_test_num']), int(cfgfile['params']['img_size']), int(cfgfile['params']['img_depth'])


# preprocess and encode image raw into tensor binary string bytes
def encode_img(_img_path, _img_size):

    # read image from disk
    img = cv2.imread(_img_path)

    # resize image to size especified
    img = cv2.resize(img, (_img_size, _img_size), interpolation=cv2.INTER_NEAREST)

    # convert image to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # convert pixels values to int
    img = img.astype(int)

    # compress back to jpg bytes
    _, img_bytes = cv2.imencode('.jpg', img)

    # return string bytes jpg
    return img_bytes.tostring()


def decode_img(_file_raw, _img_size: int, _img_depth: int):

    features = {'raw': tf.FixedLenFeature([], tf.string)}

    # Create a feature
    features = {'raw': tf.FixedLenFeature([], tf.string),
                'path': tf.FixedLenFeature([], tf.string)}

    parsed_example = tf.parse_single_example(serialized=_file_raw, features=features)

    img_raw = parsed_example['raw']
    img_path = parsed_example['path']

    # Convert the image data from string back to the numbers
    img_decoded = tf.image.decode_jpeg(img_raw)

    # Reshape image data into the original shape
    img_decoded = tf.reshape(img_decoded, [_img_size, _img_size, _img_depth])

    # convert BGR to RGB
    img_decoded = tf.reverse(img_decoded, axis=[-1])

    # converto to float32
    img_decoded = tf.cast(img_decoded, tf.float32)

    # scale pixel values to [0, 1]
    #img_decoded = img_decoded / 255

    return [img_decoded, img_path]
    #return img_decoded


def train_pipeline(_path_tfrecords, _img_size: int, _img_depth: int, _epochs: int, _batch_size: int, _cpu_count: int,
                   _shard_size: int, _shard_num: int):

    with tf.device('/cpu:0'):

        dataset = tf.data.TFRecordDataset.list_files(file_pattern=_path_tfrecords, shuffle=True, seed=False)
        dataset = dataset.shuffle(buffer_size=_shard_num, seed=False, reshuffle_each_iteration=True)
        dataset = dataset.interleave(map_func=tf.data.TFRecordDataset, cycle_length=1, block_length=1)
        dataset = dataset.map(map_func=lambda _file_raw: decode_img(_file_raw, _img_size, _img_depth),
                              num_parallel_calls=_cpu_count)
        dataset = dataset.repeat(count=_epochs)
        dataset = dataset.shuffle(buffer_size=_shard_num, seed=False, reshuffle_each_iteration=True)
        dataset = dataset.batch(batch_size=_batch_size)
        dataset = dataset.shuffle(buffer_size=_batch_size, seed=False, reshuffle_each_iteration=True)
        dataset = dataset.prefetch(buffer_size=1)

    return dataset


def simple_pipeline(_path_tfrecords, _img_size: int, _img_depth: int, _batch_size: int, _cpu_count: int):

    with tf.device('/cpu:0'):

        dataset = tf.data.TFRecordDataset(_path_tfrecords, num_parallel_reads=_cpu_count)
        dataset = dataset.map(map_func=lambda _file_raw: decode_img(_file_raw, _img_size, _img_depth),
                              num_parallel_calls=_cpu_count)
        dataset = dataset.batch(batch_size=_batch_size)

    return dataset
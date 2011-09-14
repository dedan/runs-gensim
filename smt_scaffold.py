'''
    I use this file always as a base when I write a new task or run that
    should be used with sumatra. Just to not type the same things over and
    over.
'''

from os import path
import sys
import tools


def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))



if __name__ == '__main__':
    main()
Building the module
===================

Binary packages will probably be available in the future, but currently you need
to build the ``sf`` module from source.


Building without Cython
-----------------------

If you downloaded a release that already contains the sf.cpp file, you don't
need to install Cython.

Make sure that ``USE_CYTHON`` is set to ``False`` in setup.py.  You can then
build the module by typing this command::

    python setup.py build_ext --inplace

The ``--inplace`` option means that the module will be dropped in the current
directory, which is usually more practical.


Building with Cython installed
------------------------------

If you downloaded the source straight from the Git repo or if you have
modified the source, you'll need to install Cython to build a module
including the changes.  Also, make sure that ``USE_CYTHON`` is set to
``True`` in setup.py.

When you've done so, you can build the module by typing this command::

    python setup.py build_ext --inplace

The ``--inplace`` option means that the module will be dropped in the current
directory, which is usually more practical.


Building a Python 3 module
--------------------------

It's possible to build a Python 3 module, but you may encounter two problems.

First of all, on my machine, the Cython class used in ``setup3k.py`` to
automate Cython invocation is only installed for Python 2. It's
probably possible to install it for Python 3, but it's not complicated
to invoke Cython manually::

    cython --cplus sf.pyx

The next step is to invoke the ``setup3k.py`` script to build the
module. Since we called Cython already, make sure that ``USE_CYTHON``
is set to ``False`` in ``setup3k.py``, then invoke this command::

    python3 setup3k.py build_ext --inplace

(Note that you may have to type ``python`` instead of ``python3``;
typically, GNU/Linux systems provide this as a way to call a specific
version of the interpreter, but I'm not sure that's the case for all
of them as well as Windows.)

(Also note that on GNU/Linux, the generated file won't be called
``sf.so`` but something like ``sf.cpython-32mu.so``. I don't know
about Windows.)

The second problem is that the SFML API uses raw strings a lot. This
maps well into Python 2: you just use normal string litterals most of
the time, except that when you want to use the Unicode functionality
exposed in the :py:class:`sf.Text` class.

However, in Python 3, string literals are Unicode by default, and you
need to use the ``b`` prefix if you want a raw string.  For example,
when you create a :py:class:`sf.RenderWindow`::

    window = sf.RenderWindow(video_mode, b'The title')

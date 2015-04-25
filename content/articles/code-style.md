Title: Python Code Style at We Are Wizards
Date: 2015-01-02
Category: Code
Authors: Gautier
Short_summary: I write down some of the style habits I have when when writing Python code at We Are Wizards


Here at We Are Wizards, we code review most of our commits for most of our
projects, this means readable and consistent code style helps get code
merged and ready for deployment.

In this article, I've written down some of those habits we have when writing
Python code.

## PEP8

The first rule is that we follow the
[PEP8](https://www.python.org/dev/peps/pep-0008/) unless we have a *very* good
reason not to.


## String quotes

The PEP8 suggest picking a rule about using either single-quotes or
double-quotes for strings and sticking to it. At We Are Wizards we use
single-quotes.

## Indenting long lines

PEP8 hints at using handing indents like this : 

``` python
    foo = long_function_name(var_one, var_two,
                             var_three, var_four)
```

But we prefer indenting this way :

``` python
    foo = long_function_name(
        var_one,
        var_two,
        var_three,
        var_four,
    )
```

That is : one argument per line and a trailing comma on the last line.

The first advantage is the symmetry which I find helps parsing code a little
faster.

The other advantage is that the diffs for changes affecting this code are
clearer.
Let's consider the generated diff when we remove var_four using the hanging
indent style :

``` python
    foo = long_function_name(var_one, var_two,
   -                         var_three, var_four)
   +                         var_three)
```

And let's compare it with the one argument per line style :

``` python
    foo = long_function_name(
        var_one,
        var_two,
        var_three,
   -    var_four,
    )
```

Aside from having a more correct number of lines changed, it helps finding
exactly what changed and therefore review code faster.


## Style of conditions

When writing `if` conditions, we prefer them to be formulated positively and
include an else clause.

For example, instead of the following piece of code :

``` python
    user = User.objects.filter(id=user_id).first()
    if not user or not user.has_usable_password():
        return Response(status=400)

    user.send_password_reset_email()
    return Response(status=200)
```

We prefer the following, even though it has an extra line of code :

``` python
    user = User.objects.filter(id=user_id).first()
    if user and user.has_usable_password():
        user.send_password_reset_email()
        return Response(status=200)
    else:
        return Response(status=400)
```

I find the branches more explicit with this style. It helps me think about
the various tests that should exercise this piece of code.


## Conclusion

If you have habits like these but not described here, you can share them in
the comments section.

Oyster is a programming language. It's heavily lisp-influenced (though
it becomes less lisp-like with each iteration in its production).

This particular project is an attempt at producting an interpreter for
Oyster in RPython, for translation and JIT-generation by pypy.

This go-round, rather than using a single data structure
(closure-wrapped cons cells) and attempting to describe every aspect of
a program with it, I'm playing with a much richer AST -- storing
code in a metadata-rich format, and putting a much, much greater expectaton on the
IDE to render the right information at the right time.

Because I'm just playing around, the best way to learn what I'm doing,
and what you can do, is to send me an email: [s@diiq.org](mailto:s@diiq.org)

You can also check out [on oyster](http://oyster.diiq.org), my blog about
writing artisanal lisps. 

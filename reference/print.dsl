<!DOCTYPE style-sheet PUBLIC "-//James Clark//DTD DSSSL Style Sheet//EN" [
<!ENTITY docbook PUBLIC "-//Norman Walsh//DOCUMENT DocBook Print Stylesheet//EN" CDATA DSSSL>
<!ENTITY citation SYSTEM "citation.dsl" CDATA DSSSL>
]>
<style-sheet>
<style-specification id="print" use="citation docbook">
<style-specification-body>

(define %section-autolabel% #t)
(define %default-quadding% 'justify)
(define %mono-font-family% "Courier")

(element subscript (process-children))

</style-specification-body>
</style-specification>
<external-specification id="docbook" document="docbook">
<external-specification id="citation" document="citation">
</style-sheet>

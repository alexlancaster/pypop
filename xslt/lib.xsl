<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <!-- contains a library of named templates not specific to any DTD or
 XML schema -->

 <!-- template to uppercase a node or variable -->

 <xsl:template name="upcase">
  <xsl:param name="var"/>
  <xsl:value-of select="translate($var, 'abcdefghijklmnopqrstuvwxyz',
   'ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
 </xsl:template>

 <!-- templates to calculate (number)^(power) -->

 <xsl:template name="raise-to-power">
  <xsl:param name="number"/>
  <xsl:param name="power"/>
  <xsl:call-template name="raise-to-power-iter">
   <xsl:with-param name="multiplier" select="$number"/>
   <xsl:with-param name="accumulator" select="1"/>
   <xsl:with-param name="reps" select="$power"/>
  </xsl:call-template>
 </xsl:template>

 <xsl:template name="raise-to-power-iter">
  <xsl:param name="multiplier"/>
  <xsl:param name="accumulator"/>
  <xsl:param name="reps"/>
  <xsl:choose>
   <xsl:when test="$reps &gt; 0">
    <xsl:call-template name="raise-to-power-iter">
     <xsl:with-param name="multiplier" select="$multiplier"/>
     <xsl:with-param name="accumulator" 
      select="$accumulator * $multiplier"/>
     <xsl:with-param name="reps" select="$reps - 1"/>
    </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>
    <xsl:value-of select="$accumulator"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <!-- round a number to specified decimal places -->
 <!-- by default choose current node -->
 <xsl:template name="round-to">
  <xsl:param name="node" select="."/>
  <xsl:param name="places"/>

  <!-- first check that string is, indeed, a number -->
  <xsl:choose>
   <xsl:when test= "string(number($node))='NaN'"> 

    <xsl:variable name="factor">
     <xsl:call-template name="raise-to-power">
      <xsl:with-param name="number" select="10"/>
      <xsl:with-param name="power" select="$places"/>
     </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="format">
     <xsl:call-template name="append-pad">
      <xsl:with-param name="padChar" select="'0'"/>
      <xsl:with-param name="padVar" select="'0.'"/>
      <xsl:with-param name="length" select="$places + 2"/>
     </xsl:call-template>
    </xsl:variable>
    <xsl:value-of 
     select="format-number((round($factor * $node) div $factor),
     $format)"/>
   </xsl:when>
   <!-- if not a number (NaN) return as text -->
   <xsl:otherwise><xsl:value-of select="$node"/></xsl:otherwise>
  </xsl:choose>
 </xsl:template>
 
 <xsl:template name="prepend-pad"> 
  <!-- recursive template to right justify and prepend-->
  <!-- the value with whatever padChar is passed in   -->
  <xsl:param name="padChar" select="' '"/>
  <xsl:param name="padVar"/>
  <xsl:param name="length"/>
  <xsl:choose>
   <xsl:when test="string-length($padVar) &lt; $length">
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="padChar" select="$padChar"/>
     <xsl:with-param name="padVar" select="concat($padChar,$padVar)"/>
     <xsl:with-param name="length" select="$length"/>
    </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>
    <xsl:value-of 
     select="substring($padVar,string-length($padVar) -
     $length + 1)"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>
 
 <xsl:template name="append-pad">
  <!-- recursive template to left justify and append  -->
  <!-- the value with whatever padChar is passed in   -->
  <xsl:param name="padChar" select="' '"/>
  <xsl:param name="padVar"/>
  <xsl:param name="length"/>
  <xsl:choose>
   <xsl:when test="string-length($padVar) &lt; $length">
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padChar" select="$padChar"/>
     <xsl:with-param name="padVar" select="concat($padVar,$padChar)"/>
     <xsl:with-param name="length" select="$length"/>
    </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>
    <xsl:value-of select="substring($padVar,1,$length)"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <!-- Wraps an {append, prepend-pad} to create a justified {left, -->
 <!-- right} cell.  If content is missing, use a specified noVal  -->
 <!-- (defaults to '*'). -->
 <xsl:template name="justified-cell">
  <xsl:param name="noVal" select="'*'"/>
  <xsl:param name="padVar"/>
  <xsl:param name="length"/>
  <xsl:param name="type" select="'left'"/>

  <xsl:variable name="var">
   <xsl:choose>
    <xsl:when test="$padVar">
     <xsl:value-of select="$padVar"/>
    </xsl:when>
    <xsl:otherwise>
     <xsl:value-of select="$noVal"/>
    </xsl:otherwise>
   </xsl:choose>
  </xsl:variable>
  
  <xsl:choose>
   <xsl:when test="$type='left'">
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar" select="$var"/>
     <xsl:with-param name="length" select="$length"/>
    </xsl:call-template>
   </xsl:when>

   <xsl:when test="$type='right'">
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="padVar" select="$var"/>
     <xsl:with-param name="length" select="$length"/>
    </xsl:call-template>
   </xsl:when>

   <xsl:otherwise>
    <xsl:message terminate="yes">Justified type not implemented!</xsl:message>
   </xsl:otherwise>
  </xsl:choose>
  
 </xsl:template>

 <!-- prints a newline -->
 <xsl:template name="newline"><xsl:text>
</xsl:text></xsl:template>

 <!-- separator -->
 <xsl:template name="separator">
  <xsl:call-template name="append-pad">
   <xsl:with-param name="padChar" select="'-'"/>
   <xsl:with-param name="length" select="78"/>
  </xsl:call-template>
 </xsl:template>

 <!-- finds the maximum value of a set of numeric elements, found in
 the `path' variable -->
 <xsl:template name="max-value">
  <xsl:param name="path" select="."/>
  <xsl:for-each select="$path">
   <xsl:sort select="." data-type="number" order="descending"/>
   <xsl:if test="position()=1">
    <xsl:value-of select="."/></xsl:if>
  </xsl:for-each>
 </xsl:template>

 <!-- finds the maximum string length of a set of elements, found in
 the `path' variable -->
 <xsl:template name="max-string-len">
  <xsl:param name="path" select="."/>
  <xsl:for-each select="$path">
   <xsl:sort select="string-length(.)" data-type="number" order="descending"/>
   <xsl:if test="position()=1">
    <xsl:value-of select="string-length(.)"/></xsl:if>
  </xsl:for-each>
 </xsl:template>

 <!-- finds the maximum length of an XML element (tag), found in 'path' -->
 <xsl:template name="max-tag-len">
  <xsl:param name="path" select="."/>
  <xsl:for-each select="$path">
   <xsl:sort select="string-length(name(.))" data-type="number" order="descending"/>
   <xsl:if test="position()=1">
    <xsl:value-of select="string-length(name(.))"/></xsl:if>
  </xsl:for-each>
 </xsl:template>

 <!-- get the n-th token in string with a given delimiter (default to ':') -->
 <xsl:template name="get-nth-element">
  <xsl:param name="delim" select="':'"/>
  <xsl:param name="str"/>
  <xsl:param name="n"/>

  <xsl:choose>
   <xsl:when test="$n &gt; 0">

    <!--    <xsl:message>n = <xsl:value-of select="$n"/>, str = <xsl:value-of select="$str"/></xsl:message> -->

    <xsl:call-template name="get-nth-element">
     <xsl:with-param name="delim" select="$delim"/>
     <xsl:with-param name="str" select="substring-after($str,$delim)"/>
     <xsl:with-param name="n" select="$n - 1"/>
    </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>

    <!-- if the delimiter is found in the string, we must not be at
     the end, and we return the portion before the delimter
     (e.g. 'B:'), otherwise the n-th element is the end of the string,
     in which case we simply return the current string (e.g. 'C') -->

    <xsl:choose>
     <xsl:when test="contains($str,$delim)">
      <xsl:value-of select="substring-before($str,$delim)"/>
     </xsl:when>
     <xsl:otherwise><xsl:value-of select="$str"/>
     </xsl:otherwise>
    </xsl:choose>
    
   </xsl:otherwise>
  </xsl:choose>

 </xsl:template>

 <!-- given two two columns (as strings), outputs them as adjoining -->
 <!-- each other with a specified delimiter -->
 <!--columns can be of different lengths -->
 <xsl:template name="paste-columns">
  <xsl:param name="col1"/>
  <xsl:param name="col2"/>
  <xsl:param name="delim" select="' '"/>

  <!-- make sure that both columns have text -->
  <xsl:if test="contains($col1, '&#xA;') and contains($col2, '&#xA;')">
   
   <!-- split first column into strings before and after newline -->
   <xsl:variable name="col1-before-nl">
    <xsl:if test="contains($col1, '&#xA;')">
     <xsl:value-of 
      select="substring-before($col1, '&#xA;')"/>
    </xsl:if>
   </xsl:variable>
   
   <xsl:variable name="col1-after-nl">
    <xsl:if test="contains($col1, '&#xA;')">
     <xsl:value-of 
      select="substring-after($col1, '&#xA;')"/>
    </xsl:if>
   </xsl:variable>

   <!-- split second column into strings before and after newline -->   
   <xsl:variable name="col2-before-nl">
    <xsl:if test="contains($col2, '&#xA;')">
     <xsl:value-of 
      select="substring-before($col2, '&#xA;')"/>
    </xsl:if>
   </xsl:variable>
   
   <xsl:variable name="col2-after-nl">
    <xsl:if test="contains($col2, '&#xA;')">
     <xsl:value-of 
      select="substring-after($col2, '&#xA;')"/>
    </xsl:if>
   </xsl:variable>
   
   <!-- output the concatenated strings before the newline -->
   <xsl:value-of 
    select="concat($col1-before-nl, $delim, $col2-before-nl, '&#xA;')"/>

   <!-- at least one of the remaining substrings should contain -->
   <!-- a newline -->

   <xsl:if test="contains($col1-after-nl, '&#xA;') or 
    contains($col2-after-nl, '&#xA;')">

    <!-- recursively call template -->
    <xsl:call-template name="paste-columns">
    <xsl:with-param name="col1">
     <xsl:choose>
       <!-- if we have more text in this column, use it -->
       <xsl:when test="contains($col1-after-nl, '&#xA;')">
	<xsl:value-of select="$col1-after-nl"/>
       </xsl:when>
       <!-- otherwise pass in padded string of the same width as the -->
       <!-- original string -->
       <xsl:otherwise>
	<xsl:call-template name="prepend-pad">
	 <xsl:with-param name="padVar" select="'&#xA;'"/>
	 <xsl:with-param name="length" 
	  select="string-length($col1-before-nl)"/>
	</xsl:call-template>
       </xsl:otherwise>
      </xsl:choose>
     </xsl:with-param>     
     
     <!-- likewise for column 2 -->
     <xsl:with-param name="col2">
      <xsl:choose>
       <xsl:when test="contains($col2-after-nl, '&#xA;')">
	<xsl:value-of select="$col2-after-nl"/>
       </xsl:when>
       <xsl:otherwise>
	<xsl:call-template name="prepend-pad">
	 <xsl:with-param name="padVar" select="'&#xA;'"/>
	 <xsl:with-param name="length" select="string-length($col2-before-nl)"/>
	</xsl:call-template>
       </xsl:otherwise>
      </xsl:choose>
     </xsl:with-param>
     <xsl:with-param name="delim" select="$delim"/>
    </xsl:call-template>
   </xsl:if>
  </xsl:if>
  
 </xsl:template>

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->

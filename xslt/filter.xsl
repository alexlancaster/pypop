<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <!-- ################  START FILTER OUTPUT  ############# --> 

 <xsl:template match="translateTable">

  <xsl:call-template name="newline"/>
  <xsl:text>Translations (based on alleles in Anthony Nolan database) performed:</xsl:text>

  <xsl:variable name="all-transl" select="translate"/>
  <xsl:variable name="unique-transl" select="translate[not(@input=preceding-sibling::translate/@input)]/@input"/>
  
  <xsl:call-template name="newline"/>
  <xsl:for-each select="$unique-transl">
   <xsl:value-of select="."/>
   <xsl:text>-&gt;</xsl:text>
   <xsl:value-of select="$all-transl[@input=current()]/@output"/>
   <xsl:text> (</xsl:text>
   <xsl:value-of select="count($all-transl[@input=current()])"/>
   <xsl:text>)</xsl:text>
   <xsl:if test="position()!=last()">
    <xsl:text>, </xsl:text>
   </xsl:if>
  </xsl:for-each>
   
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- ################  END FILTER OUTPUT  ############### --> 

</xsl:stylesheet>
<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 
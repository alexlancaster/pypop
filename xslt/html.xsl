<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="common.xsl"/>

 <!-- select "html" as output method -->
 <xsl:output method="html" omit-xml-declaration="yes" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd"/>

 <xsl:template match="/">
  <html>
   <head>
    <title>Population summary</title>
   </head>
   <body>
   <pre>
    <xsl:apply-templates/> 
   </pre>
   </body>
  </html>
 </xsl:template>

 <!-- sections should be at the h2 level -->
 <xsl:template name="header">
  <xsl:param name="title"/>
  <h2>
  <xsl:value-of select="$title"/>
  </h2>
 </xsl:template>

 <!-- subsections should be at the h3 level -->
 <xsl:template name="locus-header">
  <xsl:param name="title"/>
  <h3><xsl:value-of select="$title"/> [<xsl:value-of select="../@name"/>]</h3>
 </xsl:template>

 <xsl:template name="linesep-fields">
  <xsl:param name="nodes" select="*"/>

  <xsl:for-each select="$nodes">
   <strong>
   <xsl:value-of select="name(.)"/>
   <xsl:text>: </xsl:text>
   </strong>
 
   <xsl:choose>
    <xsl:when test="name(.)='pvalue'">
     <xsl:apply-templates select="."/>
    </xsl:when>
    <xsl:otherwise>
     <xsl:value-of select="."/> 
    </xsl:otherwise>
   </xsl:choose>

  <!-- if field has any attribute, print them out in brackets
   separated by commas -->
   
   <xsl:if test="@*!=''">
    <em>
    <xsl:text> (</xsl:text>
    <xsl:for-each select="@*">
     <xsl:value-of select="."/>
     <xsl:if test="position()!=last()">
      <xsl:text>, </xsl:text>
     </xsl:if>
     </xsl:for-each>
    <xsl:text>)</xsl:text>
    </em>
   </xsl:if>
   <xsl:call-template name="newline"/>
   
  </xsl:for-each>
 </xsl:template> 

 <xsl:template name="separator">
  <hr/>
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

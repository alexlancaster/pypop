<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="common.xsl"/>

 <xsl:output method="html"/>

 <!-- select "html" as output method -->
<!--

 <xsl:output method="html" omit-xml-declaration="yes" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd"/>

-->

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

 <xsl:template name="header">
  <xsl:param name="title"/>
  <xsl:value-of select="$title"/>
 </xsl:template>

 <!-- overriden <section> template -->
 <xsl:template name="section">
  <xsl:param name="level"/>
  <xsl:param name="title"/>
  <xsl:param name="text"/>
  <xsl:param name="number"/>

  <xsl:variable name="header-text">
   <xsl:call-template name="header">
    <xsl:with-param name="title">
     <xsl:if test="$number">
      <xsl:value-of select="$number"/>
      <xsl:text>. </xsl:text>
     </xsl:if>
     <xsl:value-of select="$title"/>
    </xsl:with-param>
   </xsl:call-template>
  </xsl:variable>

  <xsl:choose>
   <xsl:when test="$level=1">
    <h2><xsl:value-of select="$header-text"/></h2>
   </xsl:when> 
   <xsl:when test="$level=2">
    <h3><xsl:value-of select="$header-text"/></h3>
   </xsl:when>
   <xsl:otherwise>
    <h4><xsl:value-of select="$header-text"/></h4>
   </xsl:otherwise>
  </xsl:choose>

  <xsl:call-template name="newline"/>
  
  <xsl:if test="$text!=''">
   <xsl:call-template name="newline"/>
   <xsl:copy-of select="$text"/>
   <xsl:call-template name="newline"/>
  </xsl:if>

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

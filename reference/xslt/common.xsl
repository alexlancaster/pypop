<?xml version='1.0'?>

<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version='1.0'>

<xsl:template match="email">
  <xsl:call-template name="inline.monoseq">
   <xsl:with-param name="content">
    <xsl:text>(</xsl:text>
 
    <!-- obfuscate e-mail address -->
    <xsl:value-of select="substring-before(.,'@')"/>
    <xsl:text> at </xsl:text>
    <xsl:value-of select="substring-after(.,'@')"/>
 
    <!--  <a>
    <xsl:attribute name="href">mailto:<xsl:value-of select="."/>
   </xsl:attribute>
    <xsl:apply-templates/>
   </a>
    -->
    <xsl:text>)</xsl:text>
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>

</xsl:stylesheet>


<!--
Local variables:
mode:xml
sgml-indent-step: 1
sgml-indent-data: 1
sgml-default-dtd-file: "../../src/xslt/xsl.ced"
sgml-local-catalogs: ("catalog")
End:
-->

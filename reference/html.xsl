<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version='1.0'>
  
  <xsl:import href="http://docbook.sourceforge.net/release/xsl/snapshot/html/docbook.xsl"/>
  
 <xsl:param name="html.stylesheet" doc:type="string">style.css</xsl:param>
  
  <xsl:param name="make.valid.html" select="1"/>

  <xsl:template match="article/appendix">
    <div class="{name(.)}">
    <xsl:if test="$generate.id.attributes != 0">
      <xsl:attribute name="id">
        <xsl:call-template name="object.id"/>
      </xsl:attribute>
    </xsl:if>


    <xsl:call-template name="section.heading">
      <xsl:with-param name="level" select="2"/>
      <xsl:with-param name="title">
        <xsl:apply-templates select="." mode="object.title.markup"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:apply-templates select="appendixinfo" mode="appendix.titlepage.recto.auto.mode"/>

    <xsl:apply-templates/>
  </div>
  </xsl:template>

</xsl:stylesheet>

<!--
Local variables:
mode:xml
sgml-local-catalogs: ("catalog")
End:
-->

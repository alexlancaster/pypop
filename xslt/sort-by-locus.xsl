<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="common.xsl"/>
 
 <!-- select "text" as output method -->
 <xsl:output method="xml" omit-xml-declaration="yes"/>

 <!-- override for the moment -->
 <xsl:template name="newline"/>

 <!-- unique key for all loci -->
 <xsl:key name="loci" match="/meta/dataanalysis/locus" use="@name"/>

 <xsl:template match="/">

  <xsl:variable name="names"
   select="/meta/dataanalysis/locus[generate-id(.)=generate-id(key('loci',@name))]"/>

  <xsl:element name="output">
   <xsl:attribute name="sorted-by">locus</xsl:attribute>

   <xsl:for-each select="$names">

   <xsl:element name="locus">
    <xsl:attribute name="name">
     <xsl:value-of select="@name"/>
    </xsl:attribute>

    <xsl:call-template name="newline"/> 

    <xsl:for-each select="key('loci',@name)">
     <xsl:element name="population">
      <xsl:call-template name="newline"/> 

      <xsl:element name="filename">     
       <xsl:value-of select="../filename"/>
      </xsl:element>
      <xsl:call-template name="newline"/>

      <xsl:copy-of select="*"/>
      <xsl:call-template name="newline"/>

     </xsl:element>
     <xsl:call-template name="newline"/>

    </xsl:for-each>
   </xsl:element>
   <xsl:call-template name="newline"/>

  </xsl:for-each>

  </xsl:element>

 </xsl:template>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
